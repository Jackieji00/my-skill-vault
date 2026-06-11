---
name: universal-video-note-taker
description: 全平台视频笔记助手 v2.0。模仿 B站脚本逻辑，支持 CC/AI/Whisper 三级转录，AI 智能截图，存储至 _attachments 目录。
metadata:
  version: "2.0"
  author: Gemini CLI
---

# Universal Video Note-taker (万能视频笔记助手)

此技能模仿 Bilibili 转录脚本的稳健逻辑，实现全平台视频的自动化深度笔记。

## 核心逻辑 (Refined Patterns)

1.  **三级降级转录系统**：
    *   **Level 1**: 提取原生 CC 字幕（准确率最高）。
    *   **Level 2**: 提取 AI 自动生成字幕。
    *   **Level 3**: 提取音频并调用 `openai-whisper` 本地转录。
2.  **视觉增强**：
    *   AI 自动判断关键帧时间戳。
    *   所有图片强制保存至 `_attachments/video-notes/` 目录。
3.  **Cookie 注入**：支持 `--cookies-from-browser` 绕过小红书等平台的反爬。

## 自动化工作流

### 1. 运行环境
- 必须安装 Python 3.10+。
- 首次运行前需安装依赖：`pip install -r requirements.txt`。

### 2. 执行指令 (CLI Usage)
```bash
python scripts/processor.py --url <URL> --cookies <browser_name>
```

### 3. 康奈尔笔记布局 (Linear Layout)
生成的笔记将遵循 `EXPLANATIONS.md` 中定义的布局，确保在 Obsidian 中具备极高的易读性。

## 注意事项

- **图片路径**：笔记内引用路径必须为 `![[_attachments/video-notes/filename.jpg]]`。
- **XHS 适配**：对于小红书链接，系统会自动执行 URL 清洗，去除冗余分享参数。
