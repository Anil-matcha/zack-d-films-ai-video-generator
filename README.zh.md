<p align="right"><a href="README.md">English</a> · <b>简体中文</b></p>

# 🎬 Zack D Director

**输入一个问题或主题，全自动生成 Zack D Films 风格 3D 动画短视频 — 好奇心脚本、3D 角色三视图一致性系统、3D 关键帧渲染、Veo 3.1 视频动作生成、克隆人声旁白、关键拍放大与镜头震动特效、字幕全自动合成。**

基于 **MuAPI Platform** (`api.muapi.ai`) + 本地 `ffmpeg` 打造的 **Agent Skill**，可供任何 Coding Agent（Claude Code、Codex、Antigravity、Cursor 等）使用。

---

## 📽️ 案例视频展示 (由 MuAPI Veo 3.1 驱动)

以下是使用 **Zack D Director** 在 **MuAPI** 上端到端生成的 3D 关键帧与动画片段：

<div align="center">

https://github.com/user-attachments/assets/c20e8a61-a42d-47a7-aef1-8dc049cef3ef

<b>▶ 镜头 1 (`beat_1_a`): 男孩吞下粉色口香糖 (推进镜头)</b>

<br/><br/>

https://github.com/user-attachments/assets/7666be1e-f4c3-4040-bd4c-0fdc317152aa

<b>▶ 镜头 2 (`beat_1_b`): 食道与胃部解剖剖面 (俯仰镜头)</b>

<br/><br/>

https://github.com/user-attachments/assets/e8a8117e-ccc4-4bab-8b2a-e3f19e7581d9

<b>▶ 镜头 3 (`beat_2_a`): 微观胃酸消化过程 (右摇镜头)</b>

<br/><br/>

https://github.com/user-attachments/assets/e704bec1-3da3-4839-a176-e3a78263119e

<b>▶ 镜头 4 (`beat_2_b`): 肠道肌肉挤压过程 (定帧特写)</b>

<br/><br/>

https://github.com/user-attachments/assets/2740f2ac-99ca-4a3d-89be-4efb2e9ca75b

<b>▶ 镜头 5 (`beat_3_a`): 男孩微笑舒心结局 (拉远镜头)</b>

</div>

### 🎬 生成的动画片段与资源

| 镜头 ID | 场景 / 动作 | 镜头运动 | 关键帧海报 | 视频生成引擎 |
|---|---|---|---|---|
| **`beat_1_a`** | **男孩吞下粉色口香糖** | `push_in` (推进) | [`beat_1_a.png`](out/test_run/keyframes/beat_1_a.png) | `veo3.1-fast-image-to-video` |
| **`beat_1_b`** | **食道与胃部解剖剖面** | `tilt_down` (俯仰) | [`beat_1_b.png`](out/test_run/keyframes/beat_1_b.png) | `veo3.1-fast-image-to-video` |
| **`beat_2_a`** | **微观胃酸消化过程** | `pan_right` (右摇) | [`beat_2_a.png`](out/test_run/keyframes/beat_2_a.png) | `veo3.1-fast-image-to-video` |
| **`beat_2_b`** | **肠道肌肉挤压过程** | `static` (特写) | [`beat_2_b.png`](out/test_run/keyframes/beat_2_b.png) | `veo3.1-fast-image-to-video` |
| **`beat_3_a`** | **男孩微笑舒心结局** | `pull_out` (拉远) | [`beat_3_a.png`](out/test_run/keyframes/beat_3_a.png) | `veo3.1-fast-image-to-video` |

---

## 🔑 MuAPI 配置

设置您的 **MuAPI** API Key：
```bash
export MUAPI_API_KEY="sk-..."
```

---

## 🎬 视效与风格特点

标准的 **Zack D Films 3D 动画短视频** 风格：
- 3D 数字化角色与人体解剖剖面模型。
- 高对比度演播室光影、粘土/塑料次表面散射 (subsurface scattering)。
- 展示生物、物理或医学过程的微观剖面图 (cross-sections)。
- 好奇心闭环脚本：每一句话都抛出让人停不下的悬念。
- 极具留存感的剪辑：关键拍画面推放大 (Zoom-in)、场景切换镜头震动 (Screen Shake)、紧凑配音与字幕。

---

## 🚀 快速开始

在已安装 Skill 的 Agent 中直接输入：

> *"帮我制作一个 Zack D Films 风格的短视频，讲解吞下口香糖后身体会发生什么。"*

Agent 将自动生成脚本供您确认，随后完成三视图生成 → 3D 渲染 → 视频动作生成 → 人声克隆 → 最终剪辑合成！

---

## 📜 许可证

[MIT](LICENSE) © 2026 Zack D Director
