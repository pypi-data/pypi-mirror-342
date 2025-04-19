#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AI助手基础模块 - 提供通用工具函数和基类
"""

import os
import time
import platform
import threading
import re

# 第三方库
import pyclip
import keyboard

# 全局变量
current_chat_active = True
stop_event = threading.Event()


def clear_possible_char():
    """清除可能由快捷键输入的字符"""
    # 模拟按下退格键删除可能输入的字符
    keyboard.send('backspace')
    time.sleep(0.1)  # 短暂延迟确保退格键生效


def get_clipboard_content():
    """从剪贴板获取内容"""
    try:
        # 获取剪贴板内容
        clipboard_data = pyclip.paste()
        
        # 检查类型并正确解码
        if isinstance(clipboard_data, bytes):
            clipboard_content = clipboard_data.decode('utf-8', errors='replace')
        else:
            clipboard_content = str(clipboard_data)
            
        try:
            # 尝试将unicode转义字符串还原为中文
            if '\\u' in clipboard_content:
                clipboard_content = clipboard_content.encode('utf-8').decode('unicode_escape')
        except Exception as e:
            print(f"无法还原unicode转义字符串: {e}")
            return None
        
        # 检查剪贴板内容是否为空
        if not clipboard_content:
            print("剪贴板内容为空！")
            return None

        return clipboard_content
    except Exception as e:
        print(f"无法从剪贴板获取内容: {e}")
        return None


def type_result(text):
    """模拟键盘输入或粘贴操作"""
    config_paste = 1
    config_restore = 1

    # 模拟粘贴
    if config_paste:
        # 保存剪切板
        try:
            temp = pyclip.paste()
            if isinstance(temp, bytes):
                temp = temp.decode('utf-8')
        except:
            temp = ''

        # 复制结果
        pyclip.copy(text)

        # 粘贴结果
        if platform.system() == 'Darwin':
            keyboard.press(55)
            keyboard.press(9)
            keyboard.release(55)
            keyboard.release(9)
        else:
            keyboard.send('ctrl + v')

        # 还原剪贴板
        if config_restore:
            # 等待粘贴操作完成
            paste_delay = max(0.1, min(len(text) / 5000, 1.0))  # 根据文本长度动态调整延时
            time.sleep(paste_delay)
            pyclip.copy(temp)

    # 模拟打印
    else:
        keyboard.write(text)


def cancel_current_chat():
    """取消当前对话"""
    global current_chat_active
    current_chat_active = False
    stop_event.set()  # 设置事件，通知聊天线程停止
    print("\n当前对话已取消！")


class AIAssistantBase:
    """AI助手基类，定义通用接口和方法"""
    
    def __init__(self, model_name=None):
        """初始化AI助手
        
        Args:
            model_name: 模型名称
        """
        self.model_name = model_name
    
    def get_api_info(self):
        """获取API信息，子类必须实现此方法"""
        raise NotImplementedError("子类必须实现get_api_info方法")
    
    def chat(self, content=None):
        """与模型进行对话，子类必须实现此方法
        
        Args:
            content: 对话内容，如果为None则从剪贴板获取
        """
        raise NotImplementedError("子类必须实现chat方法")
    
    def chat_thread(self):
        """创建一个新线程来执行聊天功能"""
        global current_chat_active
        current_chat_active = True  # 重置状态为活跃
        stop_event.clear()  # 清除停止事件
        
        # 创建一个新线程来执行聊天功能
        chat_thread = threading.Thread(target=self.chat)
        chat_thread.daemon = True  # 设置为守护线程，主线程结束时自动结束
        chat_thread.start()
    
    @staticmethod
    def mask_sensitive_info(info):
        """掩盖敏感信息，只显示前4位和后4位
        
        Args:
            info: 需要掩盖的敏感信息
            
        Returns:
            掩盖后的信息
        """
        if not info:
            return None
        return info[:4] + "*" * (len(info) - 8) + info[-4:] if len(info) > 8 else "****"
