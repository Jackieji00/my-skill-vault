---
name: leetcode-sync
description: 自动同步 LeetCode 题解到题目汇总目录，并维护标准格式
version: 1.0.0
---

# LeetCode Sync Skill

此技能用于在用户于 `code/leetcode/` 目录下新增或修改题解文件时，自动同步更新到 `../../找工作/leetcode/题目` 目录下的对应题目 Markdown 文件。

## 功能特性

1. **自动解析**: 从文件名或文件内容中提取题号、标题、难度、标签、解题日期等信息。
2. **格式统一**: 使用预定义的 Markdown 模板维护题目记录。
3. **增量更新**: 如果目标文件已存在，保留历史记录并追加新的解法或心得。

## 触发条件

- 在 `code/leetcode/` 下创建或修改 `.py`, `.java`, `.cpp`, `.md` 文件。
- 文件名需包含题号，例如 `5.longest-palindromic-substring.py`。

## 核心逻辑 (Python 实现参考)

```python
import os
import re
from datetime import datetime

# 配置路径
SOURCE_DIR = "code/leetcode/"
TARGET_DIR = "../../找工作/leetcode/题目/"

def sync_problem(file_path):
    # 1. 提取基本信息
    filename = os.path.basename(file_path)
    match = re.match(r"(\d+)\.(.*)\.(py|md|cpp|java)", filename)
    if not match: return
    
    problem_id = match.group(1)
    title = match.group(2).replace("-", " ").title()
    
    # 2. 读取文件内容提取 metadata (此处仅为示例逻辑)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 假设从注释或正文中提取
    difficulty = "Medium" # 示例
    tags = ["String", "DP"] # 示例
    code = content
    
    # 3. 构造/更新目标文件
    target_filename = f"{problem_id}.{match.group(2)}.md"
    target_path = os.path.join(TARGET_DIR, target_filename)
    
    # ... 实现模板填充与文件更新逻辑 ...
    print(f"Synced {target_filename}")

```

## 使用示例

当你在 `code/leetcode/` 下保存一个新文件 `1.two-sum.py` 时，运行：
`gemini invoke leetcode-sync --file code/leetcode/1.two-sum.py`

或者配置自动化钩子以在保存时触发。
