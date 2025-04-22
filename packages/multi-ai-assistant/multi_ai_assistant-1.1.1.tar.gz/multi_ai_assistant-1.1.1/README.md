# AI 助手项目

## 项目简介

multi_ai_assistant 是一个基于 Python 的 AI 助手，支持多模型对话、TTS 语音等多种功能，适合个人效率提升及 AI 应用开发。

## 安装方法

推荐使用 pip 安装（PyPI 发布后）：

```bash
pip install multi_ai_assistant
```

或从源码安装：

```bash
git clone https://github.com/mofanx/multi_ai_assistant.git
cd multi_ai_assistant
pip install .
```

## 使用方法

安装后可通过命令行启动：

```bash
multi_ai_assistant
```

或在代码中调用：

```python
from multi_ai_assistant import AI_Assistant
assistant = AI_Assistant()
assistant.run()
```


## 依赖说明

- keyboard
- pygame
- asyncio
- requests
- openai
- pyclip
- aiohttp

## 开源协议

本项目基于 MIT 协议开源，详见 LICENSE 文件。

## 联系方式

作者：mofanx
邮箱：yanwuning@live.cn

---

本项目是一个通过快捷键调用不同AI模型进行对话的Python脚本，支持多种AI模型和TTS（文本转语音）功能。

## 功能特性

- 支持多种 AI 模型一键切换：Gemini、Qwen、QWQ、Grok、Baidu、Zhipu、Aliyun（含 Web 模式）
- 提供 TTS 语音合成功能，支持普通、流式、非流式三种模式
- 支持截图 OCR 识别、白描 OCR 识别
- 支持多角色快捷键：中英文互译、内容转 JSON、JSON 转 Markdown
- 支持 Piclab 图床上传：一键上传剪贴板图片或图片链接，自动复制 Markdown 链接到剪贴板（快捷键 F8+P）
- 通过丰富快捷键快速调用不同模型和功能
- 支持随时取消当前对话、停止 TTS、退出程序

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置环境变量

   ```
   # 需手动配置
   NEW_API_URL：New API地址
   NEW_API_KEY：New API密钥

   ALIYUN_API_KEY：阿里云API密钥
   ALIYUN_API_URL：阿里云API地址

   OTHER_TTS_BASE_URL：其他TTS API地址
   OTHER_TTS_API_KEY：其他TTS API密钥
   TTS_SERVER_BASE_URL：TTS服务器地址


   # 根据需要自行更改代码并配置
   AI_STUDIO_API_KEY：百度 AI Studio API密钥
   AI_STUDIO_API_URL：百度 AI Studio API地址

   XAI_API_URL：XAI API地址
   XAI_API_KEY：XAI API密钥
   
   ```

## 快捷键说明

| 快捷键    | 功能描述                |
|-----------|-------------------------|
| f9+o      | 调用 OpenAI 模型        |
| f9+g      | 调用 Gemini 模型        |
| f9+x      | 调用 Grok 模型          |
| f9+q      | 调用 Qwen 模型          |
| f9+w      | 调用 QWQ 模型           |
| f9+b      | 调用 Baidu 模型         |
| f9+z      | 调用 Zhipu 模型         |
| f9+a      | 调用 Aliyun 模型        |
| f9+l      | 调用 Aliyun Web 模型    |
| f9+1      | 调用 TTS 语音合成       |
| esc+1     | 停止 TTS                |
| f9+2      | 流式 TTS 语音合成       |
| f9+3      | 非流式 TTS 语音合成     |
| f8+0      | 截图 OCR 识别           |
| f8+9      | 白描 OCR 识别           |
| f8+p      | 上传剪贴板图片到Piclab  |
| f8+o      | 调用截图并上传到Piclab  |
| esc+2     | 停止流式 TTS            |
| esc+3     | 停止非流式 TTS          |
| esc       | 取消当前对话            |
| esc+f9    | 退出程序                |
| f8+e      | 翻译为英文              |
| f8+c      | 翻译为中文              |
| f8+j      | 内容转 JSON             |
| f8+m      | JSON 转 Markdown        |

## 使用方法

1. 运行主脚本：
   ```bash
   python multi_ai_assistant/ai_assistant.py
   ```

2. 按上述快捷键即可调用相应模型或功能。

3. 命令行参数：
   - `--web` 启用 Qwen Web 模式
   - `--model` 指定 OpenAI 调用的模型名称

4. 也可通过 `multi_ai_assistant` 命令或在代码中调用 `AI_Assistant()` 启动。
   | f9+1         | 调用TTS                |
   | esc+1        | 停止TTS                |
   | f9+2         | 调用流式TTS            |
   | f9+3         | 调用非流式TTS          |
   | esc          | 取消当前对话           |
   | esc+f9       | 退出程序               |

## 项目结构

```
multi_ai_assistant/
├── ai_assistant/
│   ├── assistant/                # 各类模型与功能模块
│   │   ├── __init__.py           # 子包初始化
│   │   ├── baimiao_ocr.py        # 白描 OCR 识别
│   │   ├── base.py               # 基础类定义
│   │   ├── chat_with_tts_no_stream.py  # 非流式 TTS 聊天
│   │   ├── chat_with_tts_stream.py     # 流式 TTS 聊天
│   │   ├── openai_model.py       # OpenAI 模型实现
│   │   ├── openai_tts.py         # OpenAI TTS 支持
│   │   ├── qwen_model.py         # 通义千问模型实现
│   │   ├── qwq_model.py          # QWQ 模型实现
│   │   ├── screenshot_ocr_llm.py # 截图 OCR 识别
│   │   ├── tts_client.py         # TTS 客户端
│   │   └── tts_server.py         # TTS 服务器
│   ├── __init__.py               # 包初始化文件
│   ├── ai_assistant.py           # 主程序脚本（快捷键入口等）
│   └── prompts.json              # 预设提示词配置
├── README.md                     # 项目说明文档
├── requirements.txt              # 依赖列表
├── pyproject.toml                # 构建与元数据配置
├── LICENSE                       # 开源协议文件
└── multi_ai_assistant.egg-info/  # 构建生成的元数据目录（可忽略）   
```

- 代码主入口为 `multi_ai_assistant/ai_assistant/ai_assistant.py`。
- 所有核心模型、TTS、OCR、工具均在 `multi_ai_assistant/ai_assistant/assistant/` 下实现。
- 依赖与元数据分别在 `requirements.txt` 和 `pyproject.toml` 中声明。
- `prompts.json` 为对话和功能的提示词模板。

## 贡献指南

欢迎提交Pull Request或Issue来改进本项目。

## 许可证

MIT License