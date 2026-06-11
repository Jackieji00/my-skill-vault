import os
import sys
import subprocess
import json
import re
from datetime import datetime

def clean_url(url):
    """清理 URL 中的冗余参数（特别是针对小红书和社交媒体分享链接）"""
    return url.split('?')[0]

def check_dependencies():
    """检查系统环境依赖"""
    deps = ["yt-dlp", "ffmpeg"]
    missing = []
    for dep in deps:
        if subprocess.run(["where", dep], capture_output=True).returncode != 0:
            missing.append(dep)
    return missing

def extract_metadata(url, cookie_browser=None):
    """使用 yt-dlp 获取视频元数据"""
    cmd = ["yt-dlp", "--dump-json", "--no-warnings", url]
    if cookie_browser:
        cmd.extend(["--cookies-from-browser", cookie_browser])
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    if result.returncode != 0:
        return None
    return json.loads(result.stdout)

def get_subtitles(url, cookie_browser=None):
    """三级降级转录逻辑：CC -> AI -> Whisper"""
    # 此处为逻辑说明，实际实现会调用 yt-dlp 尝试下载 srt
    print("Priority 1: Checking for CC Subtitles...")
    # ... 实现代码 ...
    print("Priority 2: Checking for AI Auto-generated Subtitles...")
    # ... 实现代码 ...
    print("Priority 3: Falling back to Local Whisper transcription...")
    # ... 调用 Whisper 模块 ...
    return "Transcribed text with timestamps..."

def capture_keyframes(video_path, timestamps, output_dir):
    """利用 ffmpeg 在关键时间点截图"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for i, ts in enumerate(timestamps):
        output_file = os.path.join(output_dir, f"frame_{i}_{datetime.now().strftime('%H%M%S')}.jpg")
        cmd = ["ffmpeg", "-ss", ts, "-i", video_path, "-frames:v", 1, "-q:v", 2, output_file, "-y"]
        subprocess.run(cmd, capture_output=True)
        print(f"Captured keyframe at {ts} -> {output_file}")

def generate_cornell_note(metadata, summary, notes, cues, images):
    """合成易读的康奈尔笔记内容"""
    # 按照 AGENTS.md 要求，保持 Human-easy-to-read
    template = f"""# {metadata.get('title', 'Video Note')}
- **Source**: {metadata.get('webpage_url', 'N/A')}
- **Author**: {metadata.get('uploader', 'Unknown')}

---

> [!abstract] 💡 核心总结 (Summary)
> {summary}

## 🏷️ 关键线索 (Cues)
{cues}

## 📝 详细笔记 (Notes)
{notes}

---
## 🎯 行动点/后续 (Next Steps)
- [ ] 复习视频关键知识点
"""
    return template

if __name__ == "__main__":
    # 模拟 CLI 运行逻辑
    pass
