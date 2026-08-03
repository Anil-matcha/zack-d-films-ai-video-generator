# Zack D Director — Agent Skill Guidelines

This directory contains an **agent skill** for generating 3D Zack D Films-style educational shorts automatically.

## Entry Point

If you are an AI Coding Agent (Claude Code, Codex, Cursor, etc.), read **[`SKILL.md`](SKILL.md)** to execute the end-to-end video production workflow.

## Skill Overview

- **Pipeline**: Trend Research → Curiosity Script → Character Consistency Sheets → 3D Keyframe Rendering → Motion Clips → Voice Cloning & Narration → FFmpeg Assembly (Zoom-ins & Screen Shakes).
- **Core Integrations**: Higgsfield MCP / API for T2I, I2V, and Voice Cloning; FFmpeg for post-processing.
- **Reference Docs**:
  - [`references/prompt-guide.md`](references/prompt-guide.md): 3D visual style rules, shaders, lighting, macro cross-sections.
  - [`references/beat-layer.md`](references/beat-layer.md): Curiosity loop script structure & pacing.
  - [`references/character-sheets.md`](references/character-sheets.md): Multi-angle visual consistency backbone.
  - [`references/voices.md`](references/voices.md): Voice cloning parameters and narrator setup.
  - [`references/models-and-gotchas.md`](references/models-and-gotchas.md): API & FFmpeg gotchas and screen shake / zoom-in filters.
