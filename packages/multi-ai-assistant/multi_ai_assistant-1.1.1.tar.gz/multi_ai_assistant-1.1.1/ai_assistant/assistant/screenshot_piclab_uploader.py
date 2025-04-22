import os
import tempfile
import pyclip
import keyboard
import platform
import subprocess
from .screenshot_ocr_llm import ScreenshotTool
from .piclab_uploader import PiclabUploader

def send_system_notification(title, message):
    """
    跨平台桌面通知，优先支持Linux，自动处理root和非root用户。
    """
    system = platform.system()
    if system == "Linux":
        try:
            if hasattr(os, "geteuid") and os.geteuid() == 0:
                current_user = os.environ.get('SUDO_USER')
                if current_user:
                    user_home = f"/home/{current_user}"
                    display = os.environ.get('DISPLAY', ':0')
                    xauthority = os.environ.get('XAUTHORITY', f"{user_home}/.Xauthority")
                    cmd = f"DISPLAY={display} XAUTHORITY={xauthority} notify-send '{title}' '{message}'"
                    subprocess.run(['su', current_user, '-c', cmd], check=True)
                else:
                    print("[通知] 无法确定实际用户，通知可能无法显示")
            else:
                subprocess.run(['notify-send', title, message], check=True)
        except Exception as e:
            print(f"[通知] 发送系统通知失败: {e}")
    else:
        print(f"[通知] {title}: {message}")

def screenshot_and_upload_piclab():
    """
    截图后自动上传到 Piclab 图床，并将 Markdown 链接复制到剪贴板
    """
    # 截图
    tool = ScreenshotTool(cache_dir_name='piclab_upload')
    screenshot_path = tool.capture_screenshot()
    if not screenshot_path or not os.path.exists(screenshot_path):
        print("截图失败，未生成图片")
        send_system_notification("截图失败", "未生成图片")
        return
    # 上传
    api_url = os.getenv('PICLAB_API_URL', 'http://localhost:3000/api/upload')
    api_key = os.getenv('PICLAB_API_KEY', 'your_api_key1')
    uploader = PiclabUploader(api_url, api_key)
    try:
        uploader.upload_image(screenshot_path)
        send_system_notification("截图上传成功", "Markdown链接已复制到剪贴板")
    except Exception as e:
        print(f"截图上传失败: {e}")
        send_system_notification("截图上传失败", str(e))
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
