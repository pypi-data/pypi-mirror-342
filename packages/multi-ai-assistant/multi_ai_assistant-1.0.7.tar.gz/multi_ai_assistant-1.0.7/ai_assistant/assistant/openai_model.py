#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
OpenAI模型实现模块
"""

import os
from openai import OpenAI

from .base import AIAssistantBase, get_clipboard_content, type_result, current_chat_active, stop_event

class OpenAIAssistant(AIAssistantBase):
    """基于OpenAI API的AI助手实现"""
    
    def __init__(self, model_name="gemini-2.0-flash", provider="default", enable_search=False, enable_stream=True, prompt=""):
        """初始化OpenAI助手
        
        Args:
            model_name: 模型名称，默认为"gemini-2.0-flash"
            provider: API提供商，可选值为"default"或"aliyun"，"xai"等
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
        elif provider == "xai":
            self.api_base = os.getenv("XAI_API_URL")
            self.api_key = os.getenv("XAI_API_KEY")
        else:
            raise ValueError(f"不支持的API提供商: {provider}")

        self.enable_search = enable_search
        self.enable_stream = enable_stream
        self.prompt = prompt
    
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
            prompt: 系统角色设定提示词，用于设置AI的行为和角色
            
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

            # 准备消息列表，如果有系统提示则添加
            messages = []
            if self.prompt:
                messages.append({"role": "system", "content": self.prompt})
            messages.append({"role": "user", "content": user_input})

            print("\n消息列表:")
            print(messages)

            # 准备请求参数
            params = {
                "model": self.model_name,
                "messages": messages
            }

            if self.enable_search:
                params["extra_body"] = {"enable_search": True}

            
            # 检查停止事件是否被设置
            if stop_event.is_set() or not current_chat_active:
                print("\n对话已取消，停止输出")
                return

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
                        # 检查是否应该继续输出
                        if not current_chat_active or stop_event.is_set():
                            print("\n对话已取消，停止输出")
                            return
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
