#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ChatWithTTS 模型实现模块
"""

import os
from openai import OpenAI
import keyboard
import asyncio
import pygame
import time

from .base import AIAssistantBase, get_clipboard_content, type_result, cancel_current_chat, clear_possible_char
from .tts_client import TTSClient

class ChatWithTTSStream(AIAssistantBase):
    """基于OpenAI API的AI助手实现"""
    
    def __init__(self, model_name="ERNIE-Speed-128K", provider="default", enable_search=False ,enable_stream=True, tts_engine="server"):
        """初始化OpenAI助手
        
        Args:
            model_name: 模型名称，默认为"hunyuan-lite"
            provider: API提供商，可选值为"default"或"aliyun"等
            enable_search: 是否启用联网搜索，默认为False
            enable_stream: 是否启用流式输出，默认为True
        """
        super().__init__(model_name)
        if provider == "default":
            self.api_base = os.getenv("NEW_API_URL")
            self.api_key = os.getenv("NEW_API_KEY")
        elif provider == "aliyun":
            self.api_base = os.getenv("ALIYUN_API_URL")
            self.api_key = os.getenv("ALIYUN_API_KEY")
        else:
            raise ValueError(f"不支持的API提供商: {provider}")

        self.enable_search = enable_search
        self.enable_stream = enable_stream
        self.segments = []
        self.response = ""
        self.tts_client = TTSClient(tts_engine=tts_engine)

        # 分段标点符号
        self.end_marks = ["。","！","？","!","?","\n\n\n"]

    def get_api_info(self):
        """获取API信息
        
        Returns:
            包含API地址和密钥的元组
        """
        masked_key = self.mask_sensitive_info(self.api_key)
        return self.api_base, masked_key
    
    def chat(self, content=None):
        """使用OpenAI API与模型对话
        
        Args:
            content: 对话内容，如果为None则从剪贴板获取
            
        Returns:
            模型的回复内容或错误信息
        """
        # 检查API配置
        api_base, masked_key = self.get_api_info()
        print("OpenAI API地址:", api_base)
        print("OpenAI API密钥:", masked_key)
        
        if not api_base:
            print("请设置环境变量 NEW_API_URL 来指定自定义API地址。")
            return
        
        if not self.api_key:
            print("请设置环境变量 NEW_API_KEY 来指定API密钥。")
            return
        
        # 从剪贴板获取用户输入
        user_input = content if content else get_clipboard_content()
        if not user_input:
            return
        
        print(f"从剪贴板获取的问题: {user_input}")
        
        try:
            # 创建OpenAI客户端实例，配置自定义API地址和密钥
            client = OpenAI(
                base_url=api_base,
                api_key=self.api_key
            )
            
            print(f"正在与模型 {self.model_name} 对话，请稍候...")
            # 使用最新的API调用方法

            params = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": user_input}]
            }

            if self.enable_search:
                params["extra_body"] = {"enable_search": True}

            if self.enable_stream:
                params["stream"] = True

                # 创建一个变量来存储完整的回复
                full_reply = ""

                # 创建一个变量来缓存流式回复
                content_buffer = ""

                print("\n模型回复:")

                # 清空之前的segments
                self.segments = []

                # 创建流式响应
                response = client.chat.completions.create(**params)

                # 处理流式响应
                for chunk in response:
                    # 检查是否有内容
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        # 打印内容片段并添加到完整回复中
                        # print(content, end="", flush=True)

                        # 输出模型流式回复
                        # type_result(content)

                        # 缓存流式回复
                        content_buffer += content

                        self.response += content

                        # 如果缓存文本包含分段标点符号
                        # 检查content_buffer中是否包含分段标点符号
                        for mark in self.end_marks:
                            if mark in content_buffer:
                                # 找到第一个分段标点符号的位置
                                end_pos = content_buffer.find(mark) + len(mark)
                                # 截取第一个字符到分段标点符号的文本
                                segment_text = content_buffer[:end_pos]
                                # 将分段文本发送到队列
                                self.segments.append(segment_text)
                                # 打印当前段落
                                print(f"\n[段落 {len(self.segments)}]: {segment_text}")
                                # 保留剩余字符到content_buffer
                                content_buffer = content_buffer[end_pos:]
                                break

                # 处理最后一个缓存
                if content_buffer:
                    self.segments.append(content_buffer)
                    print(f"\n[段落 {len(self.segments)}]: {content_buffer}")

            else:
                response = client.chat.completions.create(**params)
                
                # 获取回复内容
                reply = response.choices[0].message.content
                
                # 输出模型的回复
                print("\n模型回复:")    
                print(reply)
                # type_result(reply)
                
                return reply
        except Exception as e:
            error_msg = f"调用API时出错: {e}"
            print(error_msg)
            return error_msg

    async def process_tts_segments(self):
        """异步处理TTS段落
        
        使用流水线式处理，不等待前一个片段完全处理完成就开始处理下一个片段
        """
        # 重置状态
        self.tts_client.stop_flag = False
        
        # 初始化队列 - 确保与当前事件循环绑定
        loop = asyncio.get_running_loop()
        self.tts_client._loop = loop
        self.tts_client.segment_task = asyncio.Queue(3)  # 限制队列大小为3
        self.tts_client.speech_task = asyncio.Queue(3)
        
        # 初始化pygame
        self.tts_client._init_pygame()
        
        # 创建并运行语音生成和播放的协程
        generate_task = asyncio.create_task(self.tts_client.async_generate_speech())
        play_task = asyncio.create_task(self.tts_client.async_play_speech())
        
        # 记录任务便于后续管理
        self.tts_client.running_tasks = [generate_task, play_task]
        
        # 记录是否有文本被处理
        segments_processed = False
        
        try:
            # 处理所有文本片段
            for i, segment in enumerate(self.segments, 1):

                if not segment:
                    print("这是一个空段落")
                    continue
                
                segments_processed = True  # 标记有文本被处理
                    
                print(f"\n[发送段落 {i}/{len(self.segments)}]: {segment}")
                type_result(segment)  # 显示文本                
                
                # 清理文本并直接放入分段队列
                cleaned_text = self.tts_client.clean_text(segment)
                await self.tts_client.segment_task.put(cleaned_text)
                
                # 如果只有一个片段，等待更长时间确保它被处理
                if len(self.segments) == 1:
                    # 等待更长时间，确保生成任务有足够时间处理文本和生成语音
                    print("只有一个文本片段，等待更长时间确保处理完成")
                    await asyncio.sleep(2.0)  # 增加等待时间
                    
                    # 确保语音任务有机会被处理
                    if self.tts_client.speech_task.empty():
                        print("等待语音生成...")
                        await asyncio.sleep(1.0)  # 再等待一段时间
                    
                # 等待很短的时间，避免队列阻塞
                # 如果队列已满，等待直到有空间
                while self.tts_client.segment_task.qsize() >= 3:
                    await asyncio.sleep(0.1)
                    
                    # 检查是否需要停止
                    if keyboard.is_pressed('esc'):
                        print("用户取消了语音播放")
                        self.stop_with_tts()
                        return
            
            # 如果没有处理任何文本，直接返回
            if not segments_processed:
                print("没有文本需要处理")
                return
            
            # 等待所有队列处理完成
            # 添加超时机制，避免无限等待
            start_time = time.time()
            max_wait_time = 30.0  # 最长等待时间为30秒
            
            while not (self.tts_client.segment_task.empty() and 
                      self.tts_client.speech_task.empty() and 
                      not (pygame.mixer.get_init() and pygame.mixer.get_busy())):
                
                # # 检查是否超时
                # if time.time() - start_time > max_wait_time:
                #     print("等待TTS处理超时，强制结束")
                #     break
                
                # 定期检查是否需要停止
                if keyboard.is_pressed('esc'):
                    print("用户取消了语音播放")
                    self.stop_with_tts()
                    break
                    
                await asyncio.sleep(0.2)
                
        except Exception as e:
            print(f"TTS处理异常: {e}")
        finally:
            # 等待一小段时间，确保任务有时间完成
            if segments_processed:
                # 如果只有一个片段，等待更长时间
                if len(self.segments) == 1:
                    # 再次检查是否有语音正在播放
                    if pygame.mixer.get_init() and pygame.mixer.get_busy():
                        print("等待语音播放完成...")
                        # 等待播放完成
                        await asyncio.sleep(2.0)
                    else:
                        # 检查语音队列是否为空
                        if not self.tts_client.speech_task.empty():
                            print("等待语音播放...")
                            await asyncio.sleep(2.0)
                        else:
                            await asyncio.sleep(1.0)
                else:
                    await asyncio.sleep(0.5)
                
            # 取消协程前再等待一下，确保所有任务都有机会完成
            await asyncio.sleep(0.5)
                
            # 取消协程
            for task in self.tts_client.running_tasks:
                if not task.done():
                    task.cancel()
            
            print("所有段落已处理完成")
    
    def _run_tts_in_thread(self):
        """在新线程中运行异步TTS处理"""
        # 创建新的事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # 运行异步处理
            loop.run_until_complete(self.process_tts_segments())
        except Exception as e:
            print(f"TTS处理异常: {e}")
        finally:
            # 关闭循环
            loop.close()
    
    def start_with_tts(self):
        """启动聊天并使用TTS播放回复"""
        # 停止之前可能正在进行的TTS任务
        self.stop_with_tts()
        
        self.segments = []  # 清空之前的segments
        self.response = ""  # 清空之前的response

        # 启动聊天，获取回复并分段
        self.chat()
        
        if not self.segments:
            print("没有获取到回复内容")
            return
            
        print("\n=== 语音合成段落 ===")
        
        # 创建一个新线程来运行异步任务
        import threading
        self.tts_processing_thread = threading.Thread(target=self._run_tts_in_thread)
        self.tts_processing_thread.daemon = True  # 设置为后台线程，不阻塞主程序退出
        self.tts_processing_thread.start()
        
        # 返回前打印提示信息
        print("TTS处理已在后台启动，您可以继续操作...")
    
    def stop_with_tts(self):
        """停止当前TTS播放和处理"""
        try:
            # 停止TTS客户端的所有任务
            self.tts_client.tts_stop()
            
            # 等待一小段时间确保停止命令已被处理
            import time
            time.sleep(0.2)
            
            # 如果还有音频在播放，强制停止
            if pygame.mixer.get_init() and pygame.mixer.get_busy():
                pygame.mixer.stop()
                
            print("已停止语音播放和处理")
        except Exception as e:
            print(f"停止语音播放时出错: {e}")


# 示例用法

if __name__ == "__main__":

    print("=== AI助手已启动 ===")
    print("支持的快捷键:")
    print("f9+t: 调用TTS模型")
    print("esc: 取消当前对话输出")
    print("esc+f9: 退出程序")
    
    TTS_assistant = ChatWithTTSStream()

    keyboard.add_hotkey('f9+t', lambda: [clear_possible_char(), TTS_assistant.start_with_tts()])
    keyboard.add_hotkey('esc', lambda: [cancel_current_chat, TTS_assistant.stop_with_tts()])
    keyboard.wait('esc+f9')  # 按下 Esc+F9 键退出程序