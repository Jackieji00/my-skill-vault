---
name: obsidian-pdf-organizer
description: 自动整理 Obsidian 库中的 PDF 文件。根据库内的 requirements.md 说明书进行分档、重命名、打标签及移动到对应目录。
metadata:
  version: "1.0"
  author: Gemini CLI
---

# Obsidian PDF Organizer (PDF 自动化整理工具)

此技能用于自动化处理进入 Obsidian 库的 PDF 文件，确保所有文件严格遵守用户定义的整理规范。

## 核心守则 (The First Rule)

**必须遵守 `requirements.md` 说明书**：
在执行任何操作前，优先读取 Obsidian 库根目录（或技能 `references/` 目录）下的 `requirements.md`。该文档定义了：
1. **分类逻辑**：哪些关键词或主题属于哪个文件夹。
2. **命名规范**：文件名的格式（如 `日期-来源-标题.pdf`）。
3. **标签体系**：必须包含的标签维度（如 `#type/paper`, `#status/unread`）。
4. **GitHub 同步**：根据项目根目录要求，所有变动需考虑自动上传/推送逻辑。

## 自动化流程

### 1. 扫描与识别
- **监控路径**：默认监控 `_Inbox/` 或用户指定的待处理目录。
- **识别对象**：新出现的 `.pdf` 文件。

### 2. 内容分析 (AI-Powered)
- **多模态读取**：调用 Gemini 的视觉或文本提取能力分析 PDF 首页或全文。
- **信息提取**：提取标题、作者、日期、核心关键词、摘要。

### 3. 规则匹配
- **加载规范**：读取 `requirements.md`。
- **决策引擎**：
    - **确定路径**：根据内容匹配分类规则，确定目标文件夹。
    - **生成名称**：按照命名规范重命名文件。
    - **分配标签**：从预设标签池中选择最匹配的标签。

### 4. 执行整理
- **文件操作**：
    1. 重命名 PDF 文件。
    2. 移动文件到目标分类目录。
    3. (可选) 在同目录下创建一个同名的 `.md` 笔记文件，作为 PDF 的索引/摘要，并在其中嵌入 `![[文件名.pdf]]`。
- **元数据更新**：在生成的 `.md` 笔记或库索引文件中写入 Frontmatter 标签。

### 5. 同步与记录
- **GitHub 自动上传**：执行完毕后，检查是否需要执行 `git add`, `git commit`, `git push`（遵循项目 `requirements.md` 的“Auto-upload to GitHub”要求）。
- **更新报告**：在 Obsidian 的 `HomePage.md` 或指定日志文件中记录今日处理的 PDF 列表。

## 示例 `requirements.md` 结构参考

```markdown
# PDF 整理规范

## 1. 分类目录
- **论文 (Papers)**: 包含 Abstract, Conclusion 等学术关键词的。存放在 `Archive/Papers/`。
- **收据 (Receipts)**: 包含 Order, Invoice 等财务关键词的。存放在 `Archive/Finance/Receipts/`。
- **书籍 (Books)**: 超过 50 页且有目录结构的。存放在 `Archive/Library/`。

## 2. 命名规范
格式: `[YYYY-MM-DD]-[Category]-[Title].pdf`

## 3. 标签要求
- 所有文件必须包含 `#inbox/processed` 标签。
- 论文需包含 `#research/[领域]`。
```

## 使用方法

`gemini invoke obsidian-pdf-organizer --dir <Obsidian库路径>`
