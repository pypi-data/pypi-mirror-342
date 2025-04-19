def tts_server_request(text, engine="com.github.jing332.tts_server_android", 
                      rate=50, pitch=100, api_url="http://192.168.123.181:8325/api/tts"):
    """
    通过TTS服务器将文本转换为语音并直接播放
    
    Args:
        text: 要转换的文本
        engine: TTS引擎名称
        rate: 语速参数，范围通常为0-100
        pitch: 音调参数，范围通常为0-100
        api_url: TTS服务器API地址
        
    Returns:
        bool: 请求是否成功
    """
    import requests
    import pygame
    import os
    import tempfile
    import io
    
    # 定义请求参数
    params = {
        "text": text,
        "engine": engine,
        "rate": rate,
        "pitch": pitch
    }

    try:
        # 发送GET请求并获取返回的音频数据
        response = requests.get(api_url, params=params)
        
        # 检查请求是否成功
        if response.status_code == 200:

            # 设置 PipeWire 相关环境变量（否则使用sudo权限运行会报错：ALSA: Couldn't open audio device: Host is down）
            os.environ['PULSE_SERVER'] = 'unix:/run/user/1000/pulse/native'
            os.environ['XDG_RUNTIME_DIR'] = '/run/user/1000'
            
            # 从内存中加载音频数据
            audio_data = io.BytesIO(response.content)
            
            # 确保音频系统已初始化
            pygame.mixer.init()

            # 加载并播放音频
            pygame.mixer.music.load(audio_data)
            pygame.mixer.music.play()
            
            # 等待音频播放完成
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            print("音频播放完成")
            
            return True
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"请求出错: {e}")
        return False