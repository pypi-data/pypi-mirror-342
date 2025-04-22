#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
OpenAI TTS (文本转语音) 模块
"""

import os
import time
from openai import OpenAI
import pygame
import io
from .base import AIAssistantBase, get_clipboard_content, type_result, current_chat_active

class OpenAIAssistant(AIAssistantBase):
    """基于OpenAI API的AI助手实现"""
    
    def __init__(self, model_name="gemini-2.0-flash", provider="default", enable_search=False ,enable_stream=True):
        """初始化OpenAI助手
        
        Args:
            model_name: 模型名称，默认为"gemini-2.0-flash"
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
                print("\n模型回复:")

                # 创建流式响应
                response = client.chat.completions.create(**params)

                # 处理流式响应
                for chunk in response:
                    # 检查是否有内容
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        # 打印内容片段并添加到完整回复中
                        print(content, end="", flush=True)

                        # 输出模型流式回复
                        type_result(content)

                        full_reply += content

                # 输出完整回复
                print("\n完整回复:")
                print(full_reply)

            else:
                response = client.chat.completions.create(**params)
                
                # 获取回复内容
                reply = response.choices[0].message.content
                
                # 输出模型的回复
                print("\n模型回复:")    
                print(reply)
                type_result(reply)
                
                return reply
        except Exception as e:
            error_msg = f"调用API时出错: {e}"
            print(error_msg)
            return error_msg


class OpenAITTS(AIAssistantBase):
    """基于OpenAI API的文本转语音实现"""
    
    def __init__(self, voice="zh-CN-XiaoxiaoMultilingualNeural", model="zh-CN-XiaoxiaoMultilingualNeural", provider="default", output_format="mp3", speed=1.0):
        """初始化OpenAI TTS
        
        Args:
            voice: 语音类型，可选值为"alloy", "echo", "fable", "onyx", "nova", "shimmer"，默认为"alloy"
            model: TTS模型名称，可选值为"tts-1"或"tts-1-hd"，默认为"tts-1"
            provider: API提供商，可选值为"default"或"aliyun"等
            output_format: 输出格式，可选值为"mp3", "opus", "aac", "flac"，默认为"mp3"
            speed: 语速，范围为0.25-4.0，默认为1.0
        """
        super().__init__(model)
        self.voice = voice
        self.output_format = output_format
        self.speed = speed
        
        if provider == "default":
            self.api_base = os.getenv("OPENAI_API_BASE", "https://otts.api.zwei.de.eu.org/v1")
            self.api_key = os.getenv("OPENAI_API_KEY","sk-Zwei")
        elif provider == "openai":
            self.api_base = os.getenv("OPENAI_API_URL")
            self.api_key = os.getenv("OPENAI_API_KEY")
        else:
            raise ValueError(f"不支持的API提供商: {provider}")

    def get_api_info(self):
        """获取API信息
        
        Returns:
            包含API地址和密钥的元组
        """
        masked_key = self.mask_sensitive_info(self.api_key)
        return self.api_base, masked_key
    
    def text_to_speech(self, text=None, output_file=None):
        """将文本转换为语音
        
        Args:
            text: 要转换的文本，如果为None则从剪贴板获取
            output_file: 输出文件路径，如果为None则使用临时文件并直接播放
            
        Returns:
            生成的音频文件路径或错误信息
        """
        # 检查API配置
        api_base, masked_key = self.get_api_info()
        print("OpenAI API地址:", api_base)
        print("OpenAI API密钥:", masked_key)
        
        if not self.api_key:
            print("请设置环境变量 OPENAI_API_KEY 来指定API密钥。")
            return
        
        # 从剪贴板获取用户输入
        input_text = text if text else get_clipboard_content()
        if not input_text:
            print("没有提供文本内容！")
            return
        
        print(f"要转换的文本: {input_text[:100]}{'...' if len(input_text) > 100 else ''}")
        
        try:
            # 创建OpenAI客户端实例
            client = OpenAI(
                base_url=self.api_base,
                api_key=self.api_key
            )
            
            print(f"正在使用模型 {self.model_name} 和语音 {self.voice} 转换文本为语音，请稍候...")
            
            # 调用OpenAI TTS API
            response = client.audio.speech.create(
                model=self.model_name,
                voice=self.voice,
                input=input_text,
                response_format=self.output_format,
                speed=self.speed
            )
            
            if output_file:

                # 保存音频文件
                response.stream_to_file(output_file)
                print(f"语音已生成并保存到: {output_file}")
            
            else:
                # 将音频流保存到内存中
                audio_bytes = io.BytesIO()
                for chunk in response.iter_bytes():
                    audio_bytes.write(chunk)
                audio_bytes.seek(0)
                
                # 直接从内存播放音频
                self.play_audio(audio_bytes)
            
            return output_file
            
        except Exception as e:
            error_msg = f"调用TTS API时出错: {e}"
            print(error_msg)
            return error_msg
    
    def play_audio(self, audio_bytes):
        """播放音频数据
        
        Args:
            audio_bytes: 音频数据
        """
        try:
            print(f"正在播放音频")
            
            # 设置 PipeWire 相关环境变量（否则使用sudo权限运行会报错：ALSA: Couldn't open audio device: Host is down）
            os.environ['PULSE_SERVER'] = 'unix:/run/user/1000/pulse/native'
            os.environ['XDG_RUNTIME_DIR'] = '/run/user/1000'

            # 确保音频系统已初始化
            pygame.mixer.init()
            pygame.mixer.music.load(audio_bytes)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.quit()
            print("音频播放完成")

        except Exception as e:
            print(f"播放音频时出错: {e}")
    
    def chat(self, content=None):
        """实现基类的chat方法，实际调用text_to_speech
        
        Args:
            content: 对话内容，如果为None则从剪贴板获取
            
        Returns:
            生成的音频文件路径或错误信息
        """
        return self.text_to_speech(content)



