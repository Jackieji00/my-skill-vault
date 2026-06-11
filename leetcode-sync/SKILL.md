---
name: leetcode-sync
description: 自动同步 LeetCode 题解。支持动态路径配置，保护隐私。需遵循各目录 _Guide.md 或全局 requirements.md。
version: 1.1.0
---

# LeetCode Sync Skill

此技能用于自动化同步 LeetCode 题解代码到结构化的题目汇总笔记中。

## 隐私与路径配置 (Privacy & Path Configuration)

为了保护隐私，本技能**严禁**在代码中硬编码本地绝对路径。路径必须通过以下优先级解析：

1.  **命令行参数**: 调用时显式传入 `--src` 和 `--dest`。
2.  **环境变量**: 检查 `LEETCODE_SOURCE_DIR` 和 `LEETCODE_TARGET_DIR`。
3.  **私有内存 (Recommended)**: 检查 `MEMORY.md` (Private Project Memory) 中的路径定义。
4.  **默认值**: 仅作为回退，使用 `./code/leetcode/`。

## 核心逻辑 (Python 实现参考)

```python
import os
import re

# 动态获取路径，确保不泄露隐私
SOURCE_DIR = os.getenv("LEETCODE_SOURCE_DIR", "code/leetcode/")
TARGET_DIR = os.getenv("LEETCODE_TARGET_DIR", "../../找工作/leetcode/题目/")

def sync_problem(file_path):
    # 逻辑保持不变，但使用动态解析的 TARGET_DIR
    ...
    target_path = os.path.join(TARGET_DIR, target_filename)
    print(f"Synced {target_filename} to private directory")
```

## 使用方法

`gemini invoke leetcode-sync --file <文件路径> --src <源码目录> --dest <目标笔记目录>`
