"""
AI 助手项目

本项目是一个通过快捷键调用不同AI模型进行对话的Python脚本，支持多种AI模型和TTS（文本转语音）功能。
"""

__version__ = "1.0.2"

# 从 assistant 子包导入所有公开的类和函数
from .assistant import (
    get_clipboard_content, 
    type_result, 
    cancel_current_chat, 
    clear_possible_char,
    QwenAssistant,
    QWQAssistant,
    OpenAIAssistant,
    TTSClient,
    ChatWithTTSStream,
    ChatWithTTSNoStream,
    ScreenshotOCRLLM,
    BaimiaoScreenshotOCR
)

from .ai_assistant import AI_Assistant

# 定义公开的API
__all__ = [
    'get_clipboard_content',
    'type_result',
    'cancel_current_chat',
    'clear_possible_char',
    'QwenAssistant',
    'QWQAssistant',
    'OpenAIAssistant',
    'TTSClient',
    'ChatWithTTSStream',
    'ChatWithTTSNoStream',
    'ScreenshotOCRLLM',
    'BaimiaoScreenshotOCR',
    'BaimiaoScreenshotOCR',
    'AI_Assistant'
]

print("AI助手已导入")