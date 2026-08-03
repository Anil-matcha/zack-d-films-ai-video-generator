---
name: zackd-director
description: >
  将任意好奇心主题或问题一键生成 Zack D Films 风格的 3D 动画短视频。包含好奇心循环脚本、3D 角色/器官一致性三视图、
  3D 关键帧渲染、视频动作生成、克隆配音、关键拍放大与镜头震动特效、字幕全自动合成。
---

# 🎬 Zack D Director (中文版)

将单句主题或好奇心问题转化为完整的 **Zack D Films 风格 3D 短视频**：节奏紧凑、具有极强留存的好奇心钩子，结合 3D 角色三视图一致性系统、3D 渲染质感、克隆人声旁白、关键拍放大 (Zoom-in) 和场景过渡震动 (Screen Shake)。

由 **Higgsfield MCP / API** + 本地 **ffmpeg** 驱动。

---

## 💡 核心工作流与原则

Zack D Films 视效风格与爆款留存公式依赖以下 4 个核心支柱：

1. **好奇心闭环脚本结构 (Curiosity-Loop)**：每句话都抛出一个大脑急切想获得解答的悬念。
2. **角色与物体三视图一致性系统 (Character Sheets)**：在渲染具体场景前，先为重复出现的角色、人体器官或道具生成标准的 3D 三视图。后续所有场景均以此作为视觉锚点。
3. **标志性 3D 渲染风格**：3D 数字化艺术风格、粘土/塑料次表面散射 (subsurface scattering)、清晰的环境光遮蔽 (AO)、人体/结构剖面图 (cross-section) 及强对比光影。
4. **流体式剪辑规范**：极快剪辑节奏（每 2–4 秒一剪）、关键拍画面推进放大 (Zoom-in)、场景切换过渡震动 (Screen Shake)。

---

## 🚀 步骤指南

运行命令模式：
1. **趋势与选题**：`python scripts/trend_research.py "吞下口香糖会发生什么？"`
2. **生成脚本与镜头拆解**：`python scripts/script_generator.py out/<project> --topic "吞下口香糖会发生什么？"`
3. **生成角色/器官三视图**：`python scripts/character_sheets.py out/<project>`
4. **渲染 3D 关键帧**：`python scripts/keyframes.py out/<project>`
5. **生成视频动作**：`python scripts/clips.py out/<project>`
6. **声音克隆与旁白**：`python scripts/audio.py out/<project> --voice-sample sample.mp3`
7. **FFmpeg 最终合成**：`python scripts/assemble.py out/<project>`

详见 `SKILL.md` 与 `references/` 目录文档。
