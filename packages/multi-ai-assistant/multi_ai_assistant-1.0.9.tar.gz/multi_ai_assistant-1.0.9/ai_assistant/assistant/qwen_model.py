#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Qwen模型实现模块
"""

import os
import json
import re
import requests

from .base import AIAssistantBase, get_clipboard_content, type_result, current_chat_active, stop_event


class QwenAssistant(AIAssistantBase):
    """基于Qwen API的AI助手实现"""
    
    def __init__(self, model_name="qwen-max-latest", is_web=False):
        """初始化Qwen助手
        
        Args:
            model_name: 模型名称，默认为"qwen-max-latest"
            is_web: 是否启用web模式，添加chat_type=search参数
        """
        super().__init__(model_name)
        self.api_url = "https://chat.qwen.ai/api/chat/completions"
        self.token = os.getenv("QWEN_TOKEN")
        self.is_web = is_web
    
    def get_api_info(self):
        """获取API信息
        
        Returns:
            包含API地址和Token的元组
        """
        masked_token = self.mask_sensitive_info(self.token)
        return self.api_url, masked_token
    
    def chat_thread(self, is_web=None):
        """创建一个新线程来执行Qwen聊天功能
        
        Args:
            is_web: 是否启用web模式，如果为None则使用实例的is_web属性
        """
        global current_chat_active
        current_chat_active = True  # 重置状态为活跃
        stop_event.clear()  # 清除停止事件
        
        # 如果传入了is_web参数，则使用传入的值，否则使用实例的is_web属性
        if is_web is not None:
            self.is_web = is_web
        
        # 创建一个新线程来执行聊天功能
        import threading
        chat_thread = threading.Thread(target=self.chat)
        chat_thread.daemon = True  # 设置为守护线程，主线程结束时自动结束
        chat_thread.start()
    
    def chat(self, content=None):
        """与Qwen模型进行对话
        
        Args:
            content: 对话内容，如果为None则从剪贴板获取
            
        Returns:
            模型的回复内容或错误信息
        """
        try:
            # 设置请求头部
            headers = {
                "Authorization": f"Bearer {self.token}",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            api_url, masked_token = self.get_api_info()
            print("Qwen API地址:", api_url)
            print("Qwen Token:", masked_token)

            user_input = content if content else get_clipboard_content()
            if not user_input:
                return
                
            print(f"从剪贴板获取的问题: {user_input}")
            print(f"正在与模型 {self.model_name} 对话，请稍候...")
            
            # 构造请求参数
            params = {
                "model": self.model_name,
                "stream": True,
                "messages": [
                    {"role": "user", "content": user_input},
                ],
            }

            # 如果启用web模式，则添加 "chat_type": "search"
            if self.is_web:
                params["chat_type"] = "search"

            # 发送POST请求到API
            response = requests.post(self.api_url, headers=headers, json=params, stream=True)
            response.raise_for_status()  # 检查请求是否成功
            
            # 初始化变量
            previous_content = ""  # 用于存储之前的完整内容
            
            # 逐行处理流式响应
            for line in response.iter_lines(decode_unicode=True):
                # 检查停止事件是否被设置
                if stop_event.is_set() or not current_chat_active:
                    print("\n对话已取消，停止输出")
                    break
                    
                if line:  # 跳过空行
                    if line.startswith("data: "):  # 只处理以 "data: " 开头的行
                        json_str = line[6:]  # 去掉 "data: " 前缀
                        try:
                            data = json.loads(json_str)  # 解析 JSON
                            delta = data.get("choices", [{}])[0].get("delta", {})
                            current_content = delta.get("content", "")
                            
                            # 如果当前内容以之前内容开头，去除重复部分
                            if current_content.startswith(previous_content) and previous_content:
                                new_content = current_content[len(previous_content):]
                            else:
                                new_content = current_content
                            
                            # 仅当有新内容时才输出
                            if new_content:
                                print(new_content, end="", flush=True)  # 实时输出新增内容

                                # 去除回复中的数字引用
                                cleaned_content = re.sub(r'(\s*[\[]\d*)|(\d*[\]]+)', '', new_content)

                                # 检查是否应该继续输出
                                if not stop_event.is_set() and current_chat_active:
                                    # 流式输出
                                    type_result(cleaned_content)
                            
                            # 更新之前的完整内容
                            previous_content = current_content
                            
                        except json.JSONDecodeError:
                            print(f"\n无法解析的行: {line}")
            
            print("\n完整输出完成")

            return previous_content

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None
        except Exception as e:
            print(f"对话过程中出错: {e}")
            return None
