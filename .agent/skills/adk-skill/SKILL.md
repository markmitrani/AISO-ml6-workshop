---
name: Google ADK Development
description: Skill to develop agents with Google Agent Development Kit
---

# Google Agent Development Kit (ADK) Skill

When you are tasked with developing agents or writing code using the Google Agent Development Kit (ADK), follow these instructions strictly:

## 1. Always Read Local Framework Files First
**CRITICAL**: Before writing *any* code, you MUST explore and read the local ADK framework files within the project repository to understand its syntax, conventions, and capabilities. 

- Use tools like `list_dir`, `find_by_name`, or `grep_search` to locate the ADK framework source files or examples.
- Read through the key files using `view_file` to understand how the framework defines agents, tools, prompts, routing, and memory.
- Do not assume syntax based on general knowledge; always ground your implementation in the local ADK source files.

## 2. Implement Based on Framework Patterns
Once you understand the local syntax:
- Implement the agent following the established patterns found in the ADK files.
- Ensure all components (prompts, skill definitions, etc.) are correctly structured and placed in the appropriate directories.
