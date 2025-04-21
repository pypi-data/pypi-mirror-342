#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AI助手脚本 - 通过不同快捷键调用不同AI模型
支持模型：
- Gemini (g+f9)
- Qwen (q+f9)
- QWQ (w+f9)
- Grok (x+f9)
- Baidu (b+f9)
- Zhipu (z+f9)
- Aliyun (a+f9)
- Aliyun Web (l+f9)
"""

import argparse

# 第三方库
import keyboard
import pygame
import asyncio
import threading
import json
import os
from importlib import resources

# 导入自定义模块
from .assistant import (
    get_clipboard_content, type_result, cancel_current_chat, clear_possible_char,
    OpenAIAssistant, QwenAssistant, QWQAssistant, TTSClient, ChatWithTTSStream, ChatWithTTSNoStream
)
from .assistant.screenshot_ocr_llm import ScreenshotOCRLLM
from .assistant.baimiao_ocr import BaimiaoScreenshotOCR
from .assistant.piclab_uploader import run_on_hotkey as piclab_run_on_hotkey

# 加载提示词
with resources.open_text("ai_assistant", "prompts.json") as f:
    prompts = json.load(f)

# 提示词变量
prompt_translate_to_english = prompts["prompts"]["translate_to_english"]
prompt_translate_to_chinese = prompts["prompts"]["translate_to_chinese"]
prompt_convert_to_json = prompts["prompts"]["convert_to_json"]
prompt_convert_json_to_md = prompts["prompts"]["convert_json_to_md"]

# =========================
# 主函数
# =========================

def AI_Assistant():
    parser = argparse.ArgumentParser(description="AI助手脚本 - 通过不同快捷键调用不同AI模型")
    parser.add_argument("--web", action="store_true", help="启用Qwen的web模式，添加chat_type=search参数")
    parser.add_argument("--model", type=str, default="gemini-2.0-flash", help="指定OpenAI要调用的模型名称")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 初始化模型实例
    qwen_assistant = QwenAssistant(is_web=args.web)
    qwq_assistant = QWQAssistant()
    openai_assistant = OpenAIAssistant(model_name=args.model)
    gemini_assistant = OpenAIAssistant(model_name="gemini-2.0-flash")
    grok_assistant = OpenAIAssistant(model_name="grok-3", provider="xai")
    baidu_assistant = OpenAIAssistant(model_name="ERNIE-Speed-128K")
    # zhipu_assistant = OpenAIAssistant(model_name="GLM-4-Plus")
    zhipu_assistant = OpenAIAssistant(model_name="GLM-4-Flash")
    # aliyun_assistant = AliyunAssistant(model_name="qwen-max")
    aliyun_assistant = OpenAIAssistant(model_name="qwen-max", provider="aliyun")
    aliyun_web_assistant = OpenAIAssistant(model_name="qwen-max", provider="aliyun", enable_search=True)
    tts_client = TTSClient(tts_engine="server")
    chat_with_tts_stream = ChatWithTTSStream(model_name="qwen-max", provider="aliyun", tts_engine="server")
    chat_with_tts_no_stream = ChatWithTTSNoStream(model_name="qwen-max", provider="aliyun", tts_engine="server")
    
    # 初始化截图OCR实例
    screenshot_ocr = ScreenshotOCRLLM()
    baimiao_ocr = BaimiaoScreenshotOCR()

    # 初始化角色实例
    instance_translate_to_english = OpenAIAssistant(model_name="grok-3", provider="xai",prompt=prompt_translate_to_english)
    instance_translate_to_chinese = OpenAIAssistant(model_name="grok-3", provider="xai",prompt=prompt_translate_to_chinese)
    instance_convert_to_json = OpenAIAssistant(model_name="grok-3", provider="xai",prompt=prompt_convert_to_json)
    instance_convert_json_to_md = OpenAIAssistant(model_name="grok-3", provider="xai",prompt=prompt_convert_json_to_md)
    


    
    print("=== AI助手已启动 ===")
    print("支持的快捷键:")
    print("f9+o: 调用OpenAI模型")
    print("f9+g: 调用Gemini模型")
    print("f9+x: 调用Grok模型")
    print("f9+q: 调用Qwen模型")
    print("f9+w: 调用QWQ模型")
    print("f9+b: 调用Baidu模型")
    print("f9+z: 调用Zhipu模型")
    print("f9+a: 调用Aliyun模型")
    print("f9+l: 调用Aliyun Web模型")
    print("f9+1: 调用TTS模型")    
    print("esc+1: 停止TTS")    
    print("f9+2: 调用流式TTS")    
    print("f9+3: 调用非流式TTS")    
    print("f8+0: 调用截图OCR识别")    
    print("f8+9: 调用白描OCR识别")    
    print("esc: 取消当前对话输出")
    print("esc+f9: 退出程序")
    
    # 注册快捷键
    keyboard.add_hotkey('f9+o', lambda: [clear_possible_char(), openai_assistant.chat_thread()])    # 调用OpenAI模型
    keyboard.add_hotkey('f9+g', lambda: [clear_possible_char(), gemini_assistant.chat_thread()])    # 调用Gemini模型
    keyboard.add_hotkey('f9+x', lambda: [clear_possible_char(), grok_assistant.chat_thread()])    # 调用Grok模型
    keyboard.add_hotkey('f9+q', lambda: [clear_possible_char(), qwen_assistant.chat_thread()])    # 调用Qwen模型
    keyboard.add_hotkey('f9+w', lambda: [clear_possible_char(), qwq_assistant.chat_thread()])    # 调用QWQ模型
    keyboard.add_hotkey('f9+b', lambda: [clear_possible_char(), baidu_assistant.chat_thread()])    # 调用Baidu模型
    keyboard.add_hotkey('f9+z', lambda: [clear_possible_char(), zhipu_assistant.chat_thread()])    # 调用Zhipu模型
    keyboard.add_hotkey('f9+a', lambda: [clear_possible_char(), aliyun_assistant.chat_thread()])    # 调用Aliyun模型
    keyboard.add_hotkey('f9+l', lambda: [clear_possible_char(), aliyun_web_assistant.chat_thread()])    # 调用Aliyun Web模型
    keyboard.add_hotkey('f9+1', lambda: [clear_possible_char(), tts_client.start_tts()])    # 调用TTS
    keyboard.add_hotkey('esc+1', lambda: tts_client.tts_stop())    # 停止TTS
    keyboard.add_hotkey('f9+2', lambda: [clear_possible_char(), chat_with_tts_stream.start_with_tts()])    # 调用流式TTS
    keyboard.add_hotkey('f9+3', lambda: [clear_possible_char(), chat_with_tts_no_stream.start_with_tts()])    # 调用非流式TTS
    keyboard.add_hotkey('f8+0', lambda: [clear_possible_char(), screenshot_ocr.chat()])    # 调用截图OCR识别
    keyboard.add_hotkey('f8+9', lambda: [clear_possible_char(), baimiao_ocr.chat()])    # 调用白描OCR识别
    keyboard.add_hotkey('f8+p', lambda: piclab_run_on_hotkey())    # Piclab 图床上传
    keyboard.add_hotkey('esc+2',lambda: [cancel_current_chat, chat_with_tts_stream.stop_with_tts()]) # 停止流式TTS
    keyboard.add_hotkey('esc+3',lambda: [cancel_current_chat, chat_with_tts_no_stream.stop_with_tts()]) # 停止非流式TTS
    keyboard.add_hotkey('esc', cancel_current_chat)
    
    # 添加角色实例快捷键
    keyboard.add_hotkey('f8+e', lambda: [clear_possible_char(), instance_translate_to_english.chat_thread()])    # 调用翻译到英文
    keyboard.add_hotkey('f8+c', lambda: [clear_possible_char(), instance_translate_to_chinese.chat_thread()])    # 调用翻译到中文
    keyboard.add_hotkey('f8+j', lambda: [clear_possible_char(), instance_convert_to_json.chat_thread()])    # 调用转换为JSON
    keyboard.add_hotkey('f8+m', lambda: [clear_possible_char(), instance_convert_json_to_md.chat_thread()])    # 调用转换为Markdown
    


    # 保持脚本运行，等待按键事件
    keyboard.wait('esc+f9')  # 按下 Esc+F9 键退出程序
    print("程序已退出")

if __name__ == "__main__":
    AI_Assistant()
