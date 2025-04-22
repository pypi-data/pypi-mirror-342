import os
import tempfile
import pyclip
import keyboard
from .screenshot_ocr_llm import ScreenshotTool
from .piclab_uploader import PiclabUploader

def screenshot_and_upload_piclab():
    """
    截图后自动上传到 Piclab 图床，并将 Markdown 链接复制到剪贴板
    """
    # 截图
    tool = ScreenshotTool(cache_dir_name='piclab_upload')
    screenshot_path = tool.capture_screenshot()
    if not screenshot_path or not os.path.exists(screenshot_path):
        print("截图失败，未生成图片")
        return
    # 上传
    api_url = os.getenv('PICLAB_API_URL', 'http://localhost:3000/api/upload')
    api_key = os.getenv('PICLAB_API_KEY', 'your_api_key1')
    uploader = PiclabUploader(api_url, api_key)
    try:
        uploader.upload_image(screenshot_path)
    except Exception as e:
        print(f"截图上传失败: {e}")
    finally:
        if os.path.exists(screenshot_path):
            try:
                os.remove(screenshot_path)
            except Exception:
                pass

# 可选：直接注册快捷键（也可在主程序注册）
def run_on_hotkey():
    keyboard.add_hotkey('f8+o', screenshot_and_upload_piclab)
    print('已绑定快捷键 F8+O，截图后自动上传到 Piclab 图床')
