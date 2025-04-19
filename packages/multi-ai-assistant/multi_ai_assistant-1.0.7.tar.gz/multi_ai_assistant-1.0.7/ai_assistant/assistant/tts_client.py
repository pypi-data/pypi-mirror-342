import aiohttp
import asyncio
import io
import pygame
import re
import keyboard
from .base import get_clipboard_content
import threading
import os
import time
from typing import Optional, List, Dict, Any, Union

class TTSClient:
    """TTS客户端类，提供文本转语音功能
    
    该类实现了文本转语音的全流程，包括文本分段、API调用和语音播放。
    设计为可以轻松集成到其他项目中，并解决了事件循环绑定问题。
    """
    
    def __init__(self, tts_base_url=None, tts_api_key=None, tts_engine="api", tts_server_url=None):
        """初始化TTS客户端
        
        Args:
            tts_base_url: TTS API基础URL，如果为None则从环境变量中获取
            tts_api_key: TTS API密钥，如果为None则从环境变量中获取
            tts_engine: TTS引擎类型，可选值为 "api"(默认) 或 "server"
            tts_server_url: TTS服务器URL，仅当tts_engine为"server"时有效，默认为 TTS_SERVER_BASE_URL
        """
        # 引擎类型配置
        self.tts_engine = tts_engine
        self.tts_server_url = tts_server_url or os.getenv("TTS_SERVER_BASE_URL")
        
        # API引擎基础配置
        self.base_url = tts_base_url or os.getenv("OTHER_TTS_BASE_URL")
        self.api_key = tts_api_key or os.getenv("OTHER_TTS_API_KEY")

        print("=== TTS客户端初始化 ===")
        print(f"引擎类型: {self.tts_engine}")
        if self.tts_engine == "api":
            print(f"Base URL: {self.base_url}")
            print(f"API Key: {self.api_key}")
        else:
            print(f"TTS服务器URL: {self.tts_server_url}")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 线程和任务管理
        self.lock = threading.Lock()  # 线程锁
        
        # 线程和任务管理
        self.lock = threading.Lock()  # 线程锁
        self.tts_thread = None  # 当前运行的TTS线程
        self.running_tasks = []  # 异步任务列表
        self.stop_flag = False  # 停止标志
        
        # 异步队列 - 将在start方法中创建，确保与当前事件循环绑定
        self._loop = None  # 当前事件循环
        self.segment_task = None  # 文本分段队列
        self.speech_task = None  # 语音数据队列
        
        # 音频播放设置
        self._pygame_initialized = False
        
        # 设置 PipeWire 相关环境变量
        os.environ['PULSE_SERVER'] = 'unix:/run/user/1000/pulse/native'
        os.environ['XDG_RUNTIME_DIR'] = '/run/user/1000'

    # 清洗文本    
    def clean_text(self, text: str = None):
        """增强版文本清洗"""
        if not text:
            return ""
            
        text = re.sub(r'(\*\*|__)(.*?)\1', r'\2', text)
        text = re.sub(r'(\*|_)(.*?)\1', r'\2', text)
        text = re.sub(r'~~(.*?)~~', r'\1', text)
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^[-*]\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'^(\d+)\.\s+', lambda m: ''.join(['一', '二', '三', '四', '五', '六', '七', '八', '九', '十'][int(m.group(1))-1] if 0 < int(m.group(1)) <= 10 else m.group(1)) + '、', text, flags=re.MULTILINE)
        text = re.sub(r'(?<!\w)-(\d)', r'负\1', text)
        cleaned_text = text.strip()
        return cleaned_text

    async def split_text(self, text: str = None, max_segment_length: int = 100) -> list[str]:
        """智能分段算法，将文本分割成适合TTS处理的片段
        
        Args:
            text: 要分段的文本，如果为None则从剪贴板获取
            max_segment_length: 每个分段的最大长度
            
        Returns:
            list[str]: 分段后的文本列表
        """
        # 检查队列是否已初始化
        if not self.segment_task:
            raise RuntimeError("请先调用start方法初始化队列")
            
        # 获取文本内容
        if not text:
            print("正在从剪贴板获取文本...")
            text = get_clipboard_content()
            if not text:
                print("剪贴板为空")
                return []

        print("正在处理传入文本...")     
        # 清洗并分段文本
        cleaned_text = self.clean_text(text)
        sentences = re.split(r'(?<=[。！？\n])', cleaned_text)
        segments = []
        current_segment = ""
        
        # 处理每个句子
        for s in sentences:
            if not s or self.stop_flag:
                continue
                
            # 如果当前分段加上新句子不超过最大长度，则添加到当前分段
            if len(current_segment) + len(s) <= max_segment_length:
                current_segment += s
            else:
                # 否则完成当前分段并开始新分段
                if current_segment:
                    segments.append(current_segment)
                    await self.segment_task.put(current_segment)
                    await asyncio.sleep(0.01)  # 避免阻塞
                current_segment = s
                
        # 处理最后一个分段
        if current_segment and not self.stop_flag:
            segments.append(current_segment)
            await self.segment_task.put(current_segment)
            
        return segments

    async def async_generate_speech(self):
        """从分段队列获取文本并生成语音
        
        这是一个长时间运行的协程，会持续从segment_task队列获取文本片段，
        并调用generate_speech方法生成语音数据。
        """
        # 检查队列是否已初始化
        if not self.segment_task or not self.speech_task:
            raise RuntimeError("请先调用start方法初始化队列")
            
        # 记录是否有处理过任何文本
        has_processed_text = False
            
        try:
            while not self.stop_flag:
                try:
                    # 从队列获取文本片段，设置超时避免无限等待
                    segment = await asyncio.wait_for(self.segment_task.get(), timeout=1.0)
                    
                    # 检查是否应该停止
                    if self.stop_flag:
                        self.segment_task.task_done()
                        break
                        
                    # 生成语音
                    success = await self.generate_speech(segment)
                    if success:
                        has_processed_text = True  # 标记已处理文本
                    self.segment_task.task_done()
                    
                except asyncio.TimeoutError:
                    # 如果两个队列都为空，可能所有工作已完成
                    if self.segment_task.empty() and self.speech_task.empty():
                        # 如果已经处理过文本，等待更长时间确保音频被播放
                        if has_processed_text:
                            await asyncio.sleep(1.0)  # 等待更长时间
                            # 再次检查speech_task是否为空
                            if not self.speech_task.empty():
                                continue  # 如果还有音频等待播放，继续循环
                                
                        await asyncio.sleep(0.5)  # 再等待一段时间确认
                        if self.segment_task.empty() and self.speech_task.empty():
                            # 如果已经处理过文本但没有播放完成，再多等一会
                            if has_processed_text and pygame.mixer.get_init() and pygame.mixer.get_busy():
                                continue  # 如果正在播放，继续等待
                            break  # 所有工作完成，退出循环
                            
        except asyncio.CancelledError:
            print("语音生成任务已取消")
        except Exception as e:
            print(f"语音生成异常: {e}")

    async def generate_speech_server(self, text: str, engine: str = "com.github.jing332.tts_server_android", rate: int = 50, pitch: int = 100) -> bool:
        """使用TTS服务器生成语音数据（异步实现）
        
        Args:
            text: 要转换为语音的文本
            engine: TTS引擎名称
            rate: 语速参数，范围通常为0-100
            pitch: 音调参数，范围通常为0-100
            
        Returns:
            bool: 是否成功生成语音数据
        """
        # 检查参数和状态
        if not text or self.stop_flag or not self.speech_task:
            return False
            
        try:
            # 定义请求参数
            params = {
                "text": text,
                "engine": engine,
                "rate": str(rate),  # 确保参数是字符串类型
                "pitch": str(pitch)  # 确保参数是字符串类型
            }
            
            # 使用aiohttp发送GET请求并获取返回的音频数据
            async with aiohttp.ClientSession() as session:
                async with session.get(self.tts_server_url, params=params, timeout=10) as response:
                    # 检查请求是否成功
                    if response.status == 200:
                        # 从内存中加载音频数据
                        audio_data = io.BytesIO(await response.read())
                        
                        # 如果在读取过程中收到停止信号，则丢弃数据
                        if self.stop_flag:
                            audio_data.close()
                            return False
                            
                        # 将音频数据放入队列
                        await self.speech_task.put(audio_data)
                        print(f"已生成语音(服务器): {text[:20]}...")
                        return True
                    else:
                        print(f"TTS服务器错误: {response.status}, {await response.text()}")
                        return False
        except aiohttp.ClientError as e:
            print(f"TTS服务器连接异常: {e}")
            return False
        except Exception as e:
            print(f"TTS服务器请求异常: {e}")
            return False

    async def generate_speech(self, text: str, model: str = "zh-CN-XiaoxiaoMultilingualNeural", voice: str = "xiaoxiao", 
                             engine: str = "com.github.jing332.tts_server_android", rate: int = 50, pitch: int = 100) -> bool:
        """调用API或服务器生成语音数据
        
        Args:
            text: 要转换为语音的文本
            model: 使用的TTS模型 (API引擎使用)
            voice: 使用的语音 (API引擎使用)
            engine: TTS服务器引擎名称 (服务器引擎使用)
            rate: 语速参数，范围通常为0-100 (服务器引擎使用)
            pitch: 音调参数，范围通常为0-100 (服务器引擎使用)
            
        Returns:
            bool: 是否成功生成语音数据
        """
        # 检查参数和状态
        if not text or self.stop_flag or not self.speech_task:
            return False
        
        # 根据引擎类型选择不同的处理方式
        if self.tts_engine == "server":
            return await self.generate_speech_server(text, engine, rate, pitch)
        else:  # 默认使用API引擎
            # 准备API请求参数
            payload = {
                "model": model,
                "voice": voice,
                "input": text
            }
            
            try:
                # 发送API请求
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.base_url}/audio/speech", 
                        headers=self.headers, 
                        json=payload,
                        timeout=10
                    ) as response:
                        # 处理响应
                        if response.status == 200:
                            # 读取音频数据
                            audio_data = io.BytesIO(await response.read())
                            
                            # 如果在读取过程中收到停止信号，则丢弃数据
                            if self.stop_flag:
                                audio_data.close()
                                return False
                                
                            # 将音频数据放入队列
                            await self.speech_task.put(audio_data)
                            print(f"已生成语音(API): {text[:20]}...")
                            return True
                        else:
                            print(f"API错误: {response.status}, {await response.text()}")
                            return False
            except aiohttp.ClientError as e:
                print(f"API连接异常: {e}")
                return False
            except Exception as e:
                print(f"语音生成请求异常: {e}")
                return False

    async def async_play_speech(self):
        """从语音队列获取音频数据并播放
        
        这是一个长时间运行的协程，会持续从speech_task队列获取音频数据并播放。
        """
        # 检查队列是否已初始化
        if not self.speech_task:
            raise RuntimeError("请先调用start方法初始化队列")
            
        # 确保pygame已初始化
        self._init_pygame()
        
        # 记录是否有播放过任何音频
        has_played_audio = False
            
        try:
            while not self.stop_flag:
                try:
                    # 从队列获取音频数据，设置超时避免无限等待
                    audio_data = await asyncio.wait_for(self.speech_task.get(), timeout=1.0)
                    
                    # 检查是否应该停止
                    if self.stop_flag:
                        self.speech_task.task_done()
                        break
                    
                    # 播放音频
                    await self._play_audio(audio_data)
                    has_played_audio = True  # 标记已播放音频
                    self.speech_task.task_done()
                    print("语音播放完成")
                    
                    # 在播放完成后等待一小段时间，确保播放完全结束
                    await asyncio.sleep(0.2)
                    
                except asyncio.TimeoutError:
                    # 如果两个队列都为空，可能所有工作已完成
                    if self.segment_task and self.speech_task and \
                       self.segment_task.empty() and self.speech_task.empty():
                        # 如果正在播放，等待播放完成
                        if pygame.mixer.get_init() and pygame.mixer.get_busy():
                            await asyncio.sleep(0.5)  # 等待播放完成
                            continue
                            
                        # 如果已经播放过音频，等待更长时间确保完全结束
                        if has_played_audio:
                            await asyncio.sleep(1.0)  # 等待更长时间
                            
                        await asyncio.sleep(0.5)  # 再等待一段时间确认
                        if self.segment_task.empty() and self.speech_task.empty():
                            # 再次检查是否正在播放
                            if pygame.mixer.get_init() and pygame.mixer.get_busy():
                                continue  # 如果正在播放，继续等待
                            break  # 所有工作完成，退出循环
                            
        except asyncio.CancelledError:
            print("语音播放任务已取消")
        except Exception as e:
            print(f"语音播放异常: {e}")

    def _init_pygame(self):
        """初始化pygame音频系统"""
        if not self._pygame_initialized:
            try:
                pygame.mixer.init()
                self._pygame_initialized = True
            except Exception as e:
                print(f"初始化pygame失败: {e}")
                
    async def _play_audio(self, audio_data: io.BytesIO):
        """播放音频数据
        
        Args:
            audio_data: 要播放的音频数据
        """
        # 确保pygame mixer已初始化
        if not pygame.mixer.get_init():
            self._init_pygame()
            
        try:
            # 创建并播放声音
            sound = pygame.mixer.Sound(audio_data)
            sound.play()
            
            # 等待播放完成或被停止
            while pygame.mixer.get_busy() and not self.stop_flag:
                await asyncio.sleep(0.1)
                
            # 如果被停止，停止所有声音
            if self.stop_flag:
                pygame.mixer.stop()
                
        except Exception as e:
            print(f"播放音频异常: {e}")
            
    def tts_stop(self):
        """停止所有TTS相关任务和播放"""
        print("停止所有语音任务...")
        
        # 设置停止标志
        self.stop_flag = True
        
        # 停止音频播放
        if self._pygame_initialized and pygame.mixer.get_init():
            pygame.mixer.stop()
            print("语音播放已停止")
        
        # 清空队列
        self._clear_queues()
            
        # 取消所有正在运行的异步任务
        self._cancel_tasks()
        
    def _clear_queues(self):
        """清空所有队列"""
        if self.segment_task:
            try:
                while not self.segment_task.empty():
                    try:
                        self.segment_task.get_nowait()
                        self.segment_task.task_done()
                    except:
                        pass
            except:
                pass
                
        if self.speech_task:
            try:
                while not self.speech_task.empty():
                    try:
                        self.speech_task.get_nowait()
                        self.speech_task.task_done()
                    except:
                        pass
            except:
                pass
                
    def _cancel_tasks(self):
        """取消所有正在运行的异步任务"""
        for task in self.running_tasks:
            if not task.done():
                task.cancel()
        self.running_tasks.clear()

    async def start(self, text: str = None):
        """启动TTS处理流程
        
        Args:
            text: 要转换为语音的文本，如果为None则从剪贴板获取
        """
        # 重置状态
        self.stop_flag = False
        
        # 初始化pygame
        self._init_pygame()
        
        # 初始化队列 - 确保与当前事件循环绑定
        self._loop = asyncio.get_running_loop()
        self.segment_task = asyncio.Queue(2)
        self.speech_task = asyncio.Queue(2)
        
        
        try:
            # 创建并运行各个处理阶段的协程
            t1 = asyncio.create_task(self.split_text(text))  # 文本分段
            t2 = asyncio.create_task(self.async_generate_speech())  # 语音生成
            t3 = asyncio.create_task(self.async_play_speech())  # 语音播放
            
            # 记录任务便于后续管理
            self.running_tasks = [t1, t2, t3]
            
            # 等待所有任务完成
            await asyncio.gather(*self.running_tasks, return_exceptions=True)
        except Exception as e:
            print(f"任务执行异常: {e}")
        finally:
            print("所有语音任务已完成")

    def start_tts(self, text: str = None):
        """在新线程中启动TTS处理
        
        这是一个同步方法，可以从任何地方调用来启动TTS处理。
        会创建一个新线程来运行异步处理。
        
        Args:
            text: 要转换为语音的文本，如果为None则从剪贴板获取
        """
        # 如果已有线程在运行，先停止它
        if self.tts_thread and self.tts_thread.is_alive():
            self.tts_stop()
            # 给一点时间让线程结束
            time.sleep(0.5)
            
        # 创建新线程运行 TTS 处理
        self.tts_thread = threading.Thread(
            target=self._run_tts_in_thread,
            args=(text,),
            daemon=True
        )
        self.tts_thread.start()
        
    def _run_tts_in_thread(self, text=None):
        """在新线程中运行TTS处理"""
        with self.lock:  # 使用锁确保只有一个线程运行
            # 创建新的事件循环
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # 运行异步处理
                loop.run_until_complete(self.start(text))
            except Exception as e:
                print(f"TTS线程异常: {e}")
            finally:
                try:
                    # 关闭循环前确保所有任务已完成或已取消
                    pending = asyncio.all_tasks(loop)
                    for task in pending:
                        task.cancel()
                        
                    if pending:
                        loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
                    
                    loop.close()
                except Exception as e:
                    print(f"关闭事件循环异常: {e}")

# 示例用法
if __name__ == "__main__":
    # 设置环境变量
    # os.environ["PIPEWIRE_LATENCY"] = "128/48000"
    
    # 创建TTS客户端 (默认使用API引擎)
    tts_client = TTSClient()
    
    # 如果要使用TTS服务器引擎，可以这样初始化：
    # tts_client = TTSClient(tts_engine="server", tts_server_url="http://192.168.123.181:8325/api/tts")
    
    print("=== TTS客户端示例 ===")
    print("1. 按下 f9+5 启动TTS（从剪贴板获取文本）")
    print("2. 按下 f9+6 停止当前TTS任务")
    print("3. 按下 esc 停止当前语音播放")
    print("4. 按下 esc+5 退出程序")
    print("\n示例代码展示如何在其他项目中集成TTSClient：")
    print("""
    # 1. 导入TTSClient
    from tts_test import TTSClient
    
    # 2. 创建实例
    tts = TTSClient(api_key="你的API密钥")
    
    # 3. 使用方法1: 异步调用
    async def use_tts_async():
        await tts.start("要转换的文本")
    
    # 4. 使用方法2: 同步调用（创建新线程）
    tts.start_tts("要转换的文本")
    
    # 5. 停止TTS处理
    tts.tts_stop()
    """)
    
    # 注册热键
    keyboard.add_hotkey('esc', tts_client.tts_stop)  # ESC键停止当前语音
    keyboard.add_hotkey('f9+5', lambda: tts_client.start_tts())  # 使用新的start_tts方法
    keyboard.add_hotkey('f9+6', tts_client.tts_stop)
    
    # 等待退出
    keyboard.wait('esc+5')
    print("程序已退出")
