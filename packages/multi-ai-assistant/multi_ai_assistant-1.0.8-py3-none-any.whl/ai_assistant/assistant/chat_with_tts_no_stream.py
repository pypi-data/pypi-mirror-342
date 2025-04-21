#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ChatWithTTS 模型实现模块
"""

import os
from openai import OpenAI
import keyboard
import asyncio

from .base import AIAssistantBase, get_clipboard_content, type_result, cancel_current_chat, clear_possible_char
from .tts_client import TTSClient

class ChatWithTTSNoStream(AIAssistantBase):
    """基于OpenAI API的AI助手实现"""
    
    def __init__(self, model_name="hunyuan-lite", provider="default", enable_search=False ,enable_stream=False, tts_engine="server"):
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
        self.reply = ""
        self.tts_client = TTSClient(tts_engine=tts_engine)
        # 分段标点符号
        self.end_marks = ["。","！","？","!","?","\n"]

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

                print("\n模型流式回复:")

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
                        if any(mark in content_buffer for mark in self.end_marks):
                            # 将缓存文本发送到队列
                            self.segments.append(content_buffer)
                            # 打印当前段落
                            print(f"\n[段落 {len(self.segments)}]: {content_buffer}")
                            # 清空缓存
                            content_buffer = ""

                # 处理最后一个缓存
                if content_buffer:
                    self.segments.append(content_buffer)
                    print(f"\n[段落 {len(self.segments)}]: {content_buffer}")

            else:
                response = client.chat.completions.create(**params)
                
                # 获取回复内容
                self.reply = response.choices[0].message.content
                
                # 输出模型的回复
                print("\n模型回复:")    
                print(self.reply)
                # type_result(self.reply)
                
                return self.reply
        except Exception as e:
            error_msg = f"调用API时出错: {e}"
            print(error_msg)
            return error_msg

    def start_with_tts(self):

        all_reply = self.chat()

        print("\n完整回复：")
        print(all_reply)
        
        type_result(all_reply)

        self.tts_client.start_tts(all_reply)

    def stop_with_tts(self):
        self.tts_client.tts_stop()


if __name__ == "__main__":

    print("=== AI助手已启动 ===")
    print("支持的快捷键:")
    print("f9+t: 调用TTS模型")
    print("esc: 取消当前对话输出")
    print("esc+f9: 退出程序")
    
    TTS_assistant = ChatWithTTSNoStream()

    keyboard.add_hotkey('f9+t', lambda: [clear_possible_char(), TTS_assistant.start_with_tts()])
    keyboard.add_hotkey('esc', lambda: [cancel_current_chat, TTS_assistant.stop_with_tts()])
    keyboard.wait('esc+f9')  # 按下 Esc+F9 键退出程序