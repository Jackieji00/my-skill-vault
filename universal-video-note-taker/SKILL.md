---
name: universal-video-note-taker
description: 全平台视频笔记助手。支持多平台链接，自动提取/生成字幕，智能截取关键帧，并生成符合“康奈尔笔记法”的易读 Markdown 笔记。
metadata:
  version: "1.0"
  author: Gemini CLI
---

# Universal Video Note-taker (万能视频笔记助手)

此技能旨在将任何视频链接转化为高质量、图文并茂、且易于理解的结构化学习笔记。

## 核心能力

1.  **全平台适配**：利用 `yt-dlp` 支持 YouTube, Bilibili, Twitter, Coursera 等几乎所有视频平台。
2.  **多层级转录**：
    *   优先尝试下载内置 CC 字幕。
    *   无字幕时，调用 `ffmpeg` 提取音频并使用 AI (Whisper) 进行语音转文字。
3.  **智能图文匹配 (AI-Judgment)**：
    *   分析转录文本，识别内容切换点（如：PPT 翻页、代码演示、结论导出）。
    *   在对应时间戳利用 `ffmpeg` 截取视频关键帧图片。
4.  **康奈尔笔记模版**：生成符合人类阅读直觉的 Markdown 布局。

## 自动化工作流

### 1. 环境预检 (Dependency Check)
- 检查系统是否安装 `yt-dlp` 和 `ffmpeg`。
- 如果缺失，提示用户安装命令（如 `pip install yt-dlp` 或 `brew install ffmpeg`）。

### 2. 素材获取 (Acquisition)
- **命令参考**：`yt-dlp --write-auto-subs --skip-download <URL>`。
- 如果没有字幕，下载音频流并进行 AI 转录。

### 3. 内容分析与截图 (Analysis & Capture)
- AI 阅读全文，确定 3-5 个“高价值”时间戳。
- **截图命令**：`ffmpeg -ss [Timestamp] -i [VideoURL/File] -frames:v 1 -q:v 2 [OutputName].jpg`。

### 4. 笔记生成 (Synthesis)
使用以下 **“康奈尔笔记法 (Linear-Cornell)”** 格式：

```markdown
# [视频标题]
- **Source**: [视频链接]
- **Date**: [当前日期]

---

> [!abstract] 💡 核心总结 (Summary)
> 在最上方提供简明扼要的摘要，确保“一眼就能看懂”。

## 🏷️ 关键线索 (Cues)
- **核心概念**: [关键词]
- **关键问题**: [这部分解决了什么？]

## 📝 详细笔记 (Notes)
### 第一部分：[章节标题]
- [详细逻辑描述]
- ![关键时刻截图_01.jpg]
- **注意点**: [AI 识别出的关键细节]

### 第二部分：[章节标题]
- [逻辑演示...]
- ![关键时刻截图_02.jpg]

---
## 🎯 行动点/后续 (Next Steps)
- [ ] [AI 建议的复习或操作练习]
```

## 使用方法

`gemini invoke universal-video-note-taker --url <视频链接> --output <保存目录>`
