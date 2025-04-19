#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AI助手模块包
"""

from .base import AIAssistantBase, get_clipboard_content, type_result, cancel_current_chat, clear_possible_char
from .qwen_model import QwenAssistant
from .qwq_model import QWQAssistant
from .openai_model import OpenAIAssistant
from .tts_client import TTSClient
from .chat_with_tts_stream import ChatWithTTSStream
from .chat_with_tts_no_stream import ChatWithTTSNoStream
from .screenshot_ocr_llm import ScreenshotOCRLLM
from .baimiao_ocr import BaimiaoScreenshotOCR




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
    'BaimiaoScreenshotOCR'
]
