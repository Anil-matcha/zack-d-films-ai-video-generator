<div align="center">

<h1>🎬 Zack D Films AI Video Generator</h1>
<p><strong>Turn one question into a finished Zack D Films-style 3D animated explainer short.</strong></p>

<p>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/MuAPI-Powered-0052FF?style=for-the-badge" alt="Powered by MuAPI">
  <img src="https://img.shields.io/badge/Veo%203.1-Motion-8A2BE2?style=for-the-badge" alt="Veo 3.1 motion">
</p>
<p>
  <img src="https://img.shields.io/badge/Agent%20Skill-Claude%20Code%20%C2%B7%20Codex-d97757?style=for-the-badge" alt="Agent skill">
  <img src="https://img.shields.io/badge/FFmpeg-Assembly-4B8BBE?style=for-the-badge&logo=ffmpeg&logoColor=white" alt="FFmpeg assembly">
  <img src="https://img.shields.io/badge/License-MIT-111111?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="MIT License">
</p>

</div>

---

**Zack D Films AI Video Generator** is an agent-native production pipeline for fast, curiosity-driven 3D shorts. Give your coding agent one topic and it can plan the story, build consistent character and anatomy references, render stylized keyframes, animate them, generate narration, and assemble a vertical `final.mp4` with punchy edits.

It runs through the **MuAPI platform** (`api.muapi.ai`) with local **Python** and **ffmpeg**, and can be used from Claude Code, Codex, Cursor, Antigravity, or any agent that can follow `SKILL.md`.

> **Ask your agent:** “Make me a Zack D Films-style short explaining what happens when you swallow gum.”

## 🎥 Showcase

An end-to-end example: **“What Happens When You Swallow Gum?”**

<div align="center">

https://github.com/user-attachments/assets/c20e8a61-a42d-47a7-aef1-8dc049cef3ef

<b>▶ Shot 1 — The curiosity hook: swallowing pink gum</b>

<br/><br/>

https://github.com/user-attachments/assets/7666be1e-f4c3-4040-bd4c-0fdc317152aa

<b>▶ Shot 2 — Esophagus and stomach cutaway</b>

<br/><br/>

https://github.com/user-attachments/assets/e8a8117e-ccc4-4bab-8b2a-e3f19e7581d9

<b>▶ Shot 3 — Microscopic stomach-acid action</b>

<br/><br/>

https://github.com/user-attachments/assets/e704bec1-3da3-4839-a176-e3a78263119e

<b>▶ Shot 4 — Intestinal muscle contraction</b>

<br/><br/>

https://github.com/user-attachments/assets/2740f2ac-99ca-4a3d-89be-4efb2e9ca75b

<b>▶ Shot 5 — The resolution</b>

</div>

| Shot | Scene | Camera move | Keyframe | Motion model |
|---|---|---|---|---|
| `beat_1_a` | Boy swallowing pink gum | `push_in` | [PNG](out/test_run/keyframes/beat_1_a.png) | `veo3.1-fast-image-to-video` |
| `beat_1_b` | Esophagus and stomach cross-section | `tilt_down` | [PNG](out/test_run/keyframes/beat_1_b.png) | `veo3.1-fast-image-to-video` |
| `beat_2_a` | Stomach acid at microscopic scale | `pan_right` | [PNG](out/test_run/keyframes/beat_2_a.png) | `veo3.1-fast-image-to-video` |
| `beat_2_b` | Intestinal muscle contraction | `static` | [PNG](out/test_run/keyframes/beat_2_b.png) | `veo3.1-fast-image-to-video` |
| `beat_3_a` | Character smiling in relief | `pull_out` | [PNG](out/test_run/keyframes/beat_3_a.png) | `veo3.1-fast-image-to-video` |

## ✨ Why it works

The pipeline turns a fragmented production process into one agent-guided workflow:

- **Curiosity-first scripts** — hooks, open loops, fast pacing, and a clear payoff.
- **Consistent 3D worlds** — character turnarounds and anatomy references anchor every shot.
- **Signature visual language** — plasticine-like materials, subsurface scattering, dramatic studio light, macro depth of field, and internal cross-sections.
- **High-retention editing** — push-ins on impact beats, screen-shake transitions, voice-led pacing, music, and captions.
- **Human approval at the right moments** — review the beat map and visual direction before the expensive generation stages.
- **Agent-native by design** — the workflow, prompts, and conventions live in `SKILL.md` and `references/`.

## 🎨 The look

The visual target is a polished, stylized 3D educational short: expressive digital characters, smooth clay/plastic materials, high-contrast lighting, vibrant rim light, cinematic depth of field, and anatomical or mechanical cutaways that make invisible processes visible.

The style is established in the **keyframe stage** first. Motion is layered on afterward, so the look stays coherent from shot to shot.

## 🔄 How it works

One topic flows through a single `beats.json` project:

```
topic / question
  │
  ├─ 1. Trend research       Find curiosity-driven questions and hooks
  ├─ 2. Script breakdown      Write the beat map              ◀── GATE 1: approve
  ├─ 3. Character sheets      Build multi-angle 3D references
  ├─ 4. Keyframes             Render stylized 3D scene posters  ◀── GATE 2: choose look
  ├─ 5. Motion clips           Animate each keyframe with Veo 3.1
  ├─ 6. Voice narration        Synthesize the narration and BGM
  ├─ 7. Assembly               Add zooms, shakes, mix audio, captions
  └─ final.mp4                Vertical 9:16 short
```

## 🧩 Models and tools

| Production stage | Integration | Output |
|---|---|---|
| Topic ideas | `scripts/trend_research.py` | Curiosity-driven topic candidates |
| Story and beats | `scripts/script_generator.py` | `out/<project>/beats.json` |
| Character consistency | MuAPI image generation | 3D turnaround sheets |
| Keyframes | `nano-banana-2` with `flux-dev` fallback | One image per shot |
| Motion | `veo3.1-fast-image-to-video` with `veo3.1-image-to-video` fallback | One clip per shot |
| Narration | `minimax-speech-2.6-turbo` | Narration audio |
| Post-production | Local `ffmpeg` | Edited, captioned `final.mp4` |

## 🚀 Quick start

### 1. Install local tools

```bash
brew install ffmpeg                 # macOS
python3 -m venv .venv
source .venv/bin/activate
pip install requests pillow
```

On Windows, install `ffmpeg` and `ffprobe` with your preferred package manager instead.

### 2. Configure MuAPI

Create an API key at [muapi.ai](https://muapi.ai), then export it:

```bash
export MUAPI_API_KEY="sk-..."
```

### 3. Run it through an agent

Install or expose this repository to your coding agent, have it read [`SKILL.md`](SKILL.md), and ask for a short:

> “Create a 30-second Zack D Films-style video about why mosquitoes drink blood.”

The agent should stop for approval after the beat map and again when visual direction is ready.

### 4. Run the stages manually

```bash
# Discover or validate a topic
python3 scripts/trend_research.py "mosquitoes"

# Create and review the script breakdown
python3 scripts/script_generator.py out/mosquitoes --topic "How Mosquitoes Drink Your Blood"

# Generate references, keyframes, motion, audio, and the final cut
python3 scripts/character_sheets.py out/mosquitoes
python3 scripts/keyframes.py out/mosquitoes
python3 scripts/clips.py out/mosquitoes
python3 scripts/audio.py out/mosquitoes --voice-sample voice_recording.mp3
python3 scripts/assemble.py out/mosquitoes
```

The finished project is written to `out/mosquitoes/`, with the final render at `out/mosquitoes/final.mp4`.

## 📁 Repository structure

```
SKILL.md              Full workflow for coding agents
AGENTS.md             Entry point for Codex and other agents
README.zh.md          简体中文 documentation
references/           Style, pacing, consistency, voice, and API notes
  prompt-guide.md     3D lighting, materials, and cross-section prompts
  beat-layer.md       Curiosity-loop formulas and pacing rules
  character-sheets.md Multi-angle consistency system
  voices.md           Narration and voice setup guidance
  models-and-gotchas.md
scripts/              Pipeline automation
  trend_research.py   Topic brainstorming
  script_generator.py beats.json generation
  character_sheets.py 3D turnaround references
  keyframes.py        Scene keyframes
  clips.py            Veo 3.1 motion clips
  audio.py            Narration and BGM
  assemble.py         FFmpeg assembly and effects
examples/             Ready-to-run beat maps
out/test_run/         Included keyframe showcase assets
```

## 🧠 Agent skill details

The skill is named `zackd-director` and is documented in [`SKILL.md`](SKILL.md). It is designed for requests such as:

- “Make a Zack D Films-style 3D short.”
- “Explain this medical or scientific question as a fast animated short.”
- “Turn this topic into a curiosity-loop explainer with anatomical cutaways.”
- “Create a vertical educational video with consistent 3D characters.”

For the creative rules behind the pipeline, see [`references/prompt-guide.md`](references/prompt-guide.md), [`references/beat-layer.md`](references/beat-layer.md), and [`references/character-sheets.md`](references/character-sheets.md).

## ⚠️ Notes

- Generation stages require a working `MUAPI_API_KEY` and can incur provider costs.
- Keep API keys in environment variables; never commit them to the repository.
- The output is designed for vertical short-form video (`9:16`).
- If a provider endpoint changes, update the centralized client in [`scripts/provider.py`](scripts/provider.py).

## 📜 License

[MIT](LICENSE) © 2026 Zack D Director

## 🔗 Related

- [Vox AI Motion Graphics Generator](https://github.com/Anil-matcha/vox-ai-motion-graphics-generator) — the paper-collage explainer counterpart.
- [awesome-generative-ai-apps](https://github.com/Anil-matcha/awesome-generative-ai-apps) — more open-source AI app projects.

<div align="center">

⭐ **Star the repo if it helps you make better shorts.**

</div>
