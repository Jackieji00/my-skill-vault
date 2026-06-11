# AGENTS.md

## Project Overview

This project is an agent-driven development environment. AGENTS.md provides critical context and behavioral rules for AI coding agents working in this repository. The agent must follow these instructions at all times.


## Project Structure
```/
├── AGENTS.md # Agent instructions (this file)
├── .resource-index # Resource index file (maps resource types to directories)
├── .claude/
│ └── skills/ # Agent skill definitions
├── .codex/
│ └── skills/ # Codex-specific skill configs
├── resources/ # Resource directories (paths tracked in .resource-index)
├── requirements/ # Requirement specifications
└── tools/ # Tool definitions and scripts
```


## Build & Test Commands

- Install dependencies: `npm install` (or `pip install -r requirements.txt`)
- Run tests: `npm test` (or `pytest tests/`)
- Lint: `npm run lint` (or `ruff check .`)
- Type check: `npm run type-check` (or `mypy src/`)


## Operational Workflow: Plan-Confirm-Execute

Before performing any non-trivial task or making modifications to the codebase/resources, the agent MUST:

1.  **Formulate a Plan**: Define the steps, impact, and technical approach.
2.  **Communicate & Confirm**: Share the plan with the user and wait for explicit confirmation.
3.  **Execute**: Proceed only after the user has approved the proposed plan.


## Documentation & Logging Rules

All documentation and logs must be written in a **human-easy-to-read** format, prioritizing clarity and structural simplicity.

### 1. Work Logs (`WORK_LOG.md`)
Every project and significant subfolder must maintain a `WORK_LOG.md`.

*   **Structure**: 
    *   **Root Folder**: Records which files were modified, a brief summary of updates, and a timestamp.
    *   **Subfolders**: Records specific code-level changes, detailed logic updates, and timestamps.
*   **Behavior**: 
    *   **Append-Only**: Only add new entries. Never modify or delete existing historical logs.
    *   **Newest First**: Always prepend the latest update to the top of the file.
*   **Format**: `[Timestamp] | [File/Module] | [Action Summary/Detail]`

### 2. Explanation Files (`EXPLANATIONS.md`)
Every project and subfolder must maintain an `EXPLANATIONS.md` that serves as a living document of the system's design.

*   **Structure**:
    *   **Root Folder**: High-level overview. What is this project for? What are its core features?
    *   **Subfolders**: Detailed technical implementation. How is the functionality achieved?
        *   Detailed documentation for every **Method/Function**.
        *   Clear definitions of **Inputs** and **Outputs**.
        *   Description of the **Internal Logic** and flow of each method.
*   **Behavior**: This file can be continuously updated and refactored to reflect the current state of the code.


## Code Style & Conventions

- Language: TypeScript / Python 3.10+
- Use explicit type annotations for all function signatures
- Follow existing patterns when adding new files; do not introduce new patterns without updating this AGENTS.md
- Keep functions small and focused; prefer composition over inheritance
- Add docstrings/comments for any non-obvious logic
- Run linter before committing changes


## Resource & Index File Management

This project maintains a resource index file that tracks where specific types of resources are stored.

### Resource Index File

The resource index file is located at: **`.resource-index`**

This file contains a mapping of resource types to their corresponding directory paths. When you need to locate where a particular type of resource is stored, read `.resource-index` first.

### New Resource Registration

When you create a new resource (skill, requirement, tool, template, etc.), you **MUST**:

1. Add an entry to `.resource-index` mapping the resource type to its location
2. Place the resource in the directory specified by its mapping
3. If no mapping exists for that resource type, create one with an appropriate directory path

### Modification Rules

Before modifying any file under a resource directory (e.g., `.claude/skills/`, `requirements/`, `tools/`), you MUST:

1. Check if a **requirement file** exists in that directory
2. If a requirement file is present, read it first to understand the constraints and specifications for that resource
3. Ensure any modifications comply with the requirements defined in that file

**Requirement file naming conventions** (check in this order):
- `REQUIREMENTS.md` — General requirements for the directory
- `spec.md` — Specification document
- `constraints.md` — Constraint definitions
- Any `.req.md` file — Requirement markdown file


## GitHub Repository Management

This project is tracked in a GitHub repository. Any modifications to files or folders within this repo MUST be automatically committed and pushed to GitHub.

### Auto-Commit & Push Rules

After completing ANY file modification, creation, or deletion within the repository, you MUST:

1. **Stage the changes**: `git add -A`
2. **Commit with a descriptive message**: `git commit -m "<type>(<scope>): <description>"`
3. **Push to remote**: `git push`

### Commit Message Format

Follow this format for all auto-commits:
```<type>(<scope>): <subject>

[optional body]```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`.

### When to Commit

Trigger an auto-commit after:
- Creating, modifying, or deleting any file
- Updating `.resource-index` or any requirement file
- Any change that would affect the repository's state


## Security & Boundaries

- Never hardcode secrets, API keys, or credentials.
- Never commit `.env` files.
- Do not modify files outside the project root.
- Do not delete or overwrite `.resource-index` unless explicitly instructed.
- **Auto-commit and push are MANDATORY** for all repository changes.


## 规则解释（供人类维护者参考）

### 关于日志与文档
1. **WORK_LOG.md**: 记录“做了什么”。采用增量式，最新的在最上面，且不可删改历史。
2. **EXPLANATIONS.md**: 记录“是怎么做的”。需要详细到函数签名、输入输出和内部逻辑，方便人类阅读。

### 关于工作流
AI 在动手前必须先提供计划并获得人类确认（Plan-Confirm-Execute）。

### 关于 GitHub 自动上传
所有变更必须立即 commit 并 push，确保代码库实时同步。
