# Project Explanation: My Skill Vault

## Overview
`my-skill-vault` is a centralized repository for Gemini CLI skills. It serves as an "agentic brain" where specialized workflows are stored, versioned, and shared across different workspaces.

## Core Features
- **Automation Workflows**: Pre-defined sequences for complex tasks like daily routines and document organization.
- **Rule-Based Processing**: Deep integration with user-defined requirements and maintenance guides.
- **Obsidain Integration**: Specialized for managing knowledge within Obsidian vaults.
- **GitHub Auto-Sync**: Mandatory state synchronization to ensure the vault is always backed up and versioned.

## System Architecture
- **Skills**: Modular packages containing instructions (`SKILL.md`) and optional resources.
- **Requirements**: A hierarchical rule system where root `requirements.md` defines global taboos and sub-folder `_Guide.md` defines specific local logic.
- **Agents**: AI entities (like this one) governed by `AGENTS.md` to ensure predictable and safe operations.
