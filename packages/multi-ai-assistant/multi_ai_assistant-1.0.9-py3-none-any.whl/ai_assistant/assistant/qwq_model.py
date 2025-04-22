#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
QWQ模型实现模块
"""

import os
from openai import OpenAI

from .base import AIAssistantBase, get_clipboard_content, type_result, current_chat_active, stop_event


class QWQAssistant(AIAssistantBase):
    """基于QWQ API的AI助手实现"""
    
    def __init__(self, model_name="qwq"):
        """初始化QWQ助手
        
        Args:
            model_name: 模型名称，默认为"qwq"
        """
        super().__init__(model_name)
        self.api_base = os.getenv("AI_STUDIO_API_URL")
        self.api_key = os.getenv("AI_STUDIO_API_KEY")
    
    def get_api_info(self):
        """获取API信息
        
        Returns:
            包含API地址和密钥的元组
        """
        masked_key = self.mask_sensitive_info(self.api_key)
        return self.api_base, masked_key
    
    def chat(self, content=None):
        """与QWQ模型进行对话
        
        Args:
            content: 对话内容，如果为None则从剪贴板获取
            
        Returns:
            模型的回复内容或错误信息
        """
        global current_chat_active
        try:
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.api_base
            )
            
            api_base, masked_key = self.get_api_info()
            print("QWQ API地址:", api_base)
            print("QWQ API密钥:", masked_key)
            
            # 获取剪贴板内容
            user_input = content if content else get_clipboard_content()
            if not user_input:
                print("无法获取剪贴板内容，取消对话")
                current_chat_active = False
                return

            print(f"从剪贴板获取的问题: {user_input}")
            print("正在与QWQ模型对话，请稍候...")
            
            completion = client.chat.completions.create(
                model=self.model_name,
                temperature=0.6,
                messages=[
                    {"role": "user", "content": user_input}
                ],
                stream=True
            )

            # 处理流式响应
            for chunk in completion:
                # 检查停止事件是否被设置
                if stop_event.is_set() or not current_chat_active:
                    print("\n对话已取消，停止输出")
                    break
                
                if hasattr(chunk.choices[0].delta, "reasoning_content") and chunk.choices[0].delta.reasoning_content:
                    # 如果有推理结果，输出推理结果
                    print(chunk.choices[0].delta.reasoning_content, end="", flush=True)
                    type_result(chunk.choices[0].delta.reasoning_content)
                elif hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                    # 否则输出生成结果
                    print(chunk.choices[0].delta.content, end="", flush=True)
                    type_result(chunk.choices[0].delta.content)
        except Exception as e:
            print(f"\n对话过程中出错: {e}")
        finally:
            # 确保在函数结束时重置状态
            current_chat_active = True
