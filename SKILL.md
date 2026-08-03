---
name: zackd-director
description: >
  Turn ONE curiosity-driven topic or question into a finished Zack D Films-style 3D animated short video, end to end
  on Higgsfield MCP / API + local ffmpeg — curiosity-loop script, character consistency sheets, 3D keyframe rendering,
  motion clips, cloned voiceover, zoom-ins, screen shakes, and captions, all automated. Use this whenever the user wants a
  "Zack D Films style short", a 3D medical / anatomical / educational explainer short, a curiosity-driven short video,
  or wants to automate 3D animated short production with Higgsfield.
  Triggers: "zack d films short", "zack d style", "3d animation short", "curiosity loop video", "make a zack d video",
  "turn this topic into a zack d short".
---

# 🎬 Zack D Director

Turn a single topic or question into a finished **Zack D Films-style 3D short video**: a fast-paced, curiosity-hooking, 3D animated short where every line opens a question your brain needs closed, supported by consistent 3D character sheets, high-impact motion, cloned voice narration, key-beat zoom-ins, and screen shakes between scenes.

Powered by **MuAPI Platform (api.muapi.ai)** + **Google Veo 3.1** + local **ffmpeg**.

---

## 💡 The Core Workflow & Principles

The Zack D Films visual style and viral retention formula rely on 4 critical pillars:

1. **Curiosity-Loop Script Structure**: Every sentence opens an open loop (a question your brain physically needs answered), driving scroll-stopping retention.
2. **Character & Object Consistency Sheets**: Recurring characters, anatomical parts, or items are rendered on standard 3D turnaround sheets first. Every scene uses these sheets as visual anchors to guarantee exact visual identity across angles and wear.
3. **Signature 3D Render Style**: Stylized 3D digital art, smooth clay/plasticine subsurface scattering, crisp ambient occlusion, cross-section views, vibrant lighting, and cinematic depth of field.
4. **Fluid Editing Conventions**: Fast cuts (every 2–4 seconds), camera zoom-ins on key impact beats, and screen shakes on scene transitions.

---

## 🛠️ Prerequisites

1. **MuAPI Key Setup**:
   - `export MUAPI_API_KEY="sk-..."` (get your key at https://muapi.ai)
2. **Local Tools**:
   - `ffmpeg` + `ffprobe` (for video assembly, zoompans, screen shakes, sound ducking).
   - Python 3 with `Pillow` (for text overlays and image processing).
3. **Cloned Voice Sample**:
   - ~60 seconds of clean voice recording for zero-shot voice cloning.

---

## 🚀 Step-by-Step Production Pipeline

Each project lives under `out/<project>/` and is governed by `beats.json`.

```
topic / trend
  │
  ├─ 1. trend & curiosity hook  Claude researches / formulates curiosity questions
  ├─ 2. script breakdown         Generate beats.json with scene details & asset requirements ◀── GATE 1: User approves script
  ├─ 3. character sheets         Generate orthographic turnaround reference sheets
  ├─ 4. 3D keyframes             Render keyframe images anchored to character sheets
  ├─ 5. motion clips             Animate keyframes via Higgsfield image-to-video
  ├─ 6. voice narration          Synthesize full script in user's cloned voice
  ├─ 7. assembly                 FFmpeg: concat clips, zoom-ins, screen shakes, captions, BGM
  └─ final.mp4
```

### Step 1: Trend Research & Topic Selection
Run trend research to identify high-curiosity medical, scientific, or everyday questions:
```bash
python scripts/trend_research.py "Why do your ears pop on airplanes?"
```
*Outputs proposed topics with curiosity hooks.*

### Step 2: Curiosity Script & Scene Breakdown
Generate `out/<project>/beats.json`:
```bash
python scripts/script_generator.py out/<project> --topic "What Happens When You Swallow Gum?"
```
*Beats checklist*:
- **Beat 1**: Hook (≤3s). Opens the curiosity loop.
- **Pacing**: Cuts every 2–4s (2 shots per beat: wide establishing + close-up detail).
- **Scene specifications**: Explicit camera focus, character actions, and cross-section requirements.
- **GATE 1**: Show the `beats.json` breakdown to the user for approval.

### Step 3: Character Consistency Sheets
Generate 3D character/asset reference sheets for all recurring elements:
```bash
python scripts/character_sheets.py out/<project>
```
*Creates orthographic front/side/back 3D reference images under `out/<project>/characters/`.*

### Step 4: 3D Keyframe Rendering
Render beat keyframes using the character sheets as visual backbones:
```bash
python scripts/keyframes.py out/<project>
```
*Ensures 3D stylized lighting, subsurface scattering, and exact character identity.*

### Step 5: Motion Clip Generation
Animate keyframes with Higgsfield Image-to-Video:
```bash
python scripts/clips.py out/<project>
```
*Applies smooth camera motions, internal element animations, and macro zoom shifts.*

### Step 6: Voice Cloning & Narration
Synthesize narration in the cloned voice:
```bash
python scripts/audio.py out/<project> --voice-sample voice_recording.mp3
```
*Produces seamless narration timed beat-by-beat.*

### Step 7: Final Cut Assembly
Assemble the video with signature Zack D editing effects:
```bash
python scripts/assemble.py out/<project>
```
- Adds **zoom-ins** on key beats.
- Applies **screen shakes** between scene transitions.
- Duck background music under narration and burn styled captions.
- Outputs `out/<project>/final.mp4`.

---

## 📚 References & Resources

- [`references/prompt-guide.md`](references/prompt-guide.md): 3D visual style prompt guidelines.
- [`references/beat-layer.md`](references/beat-layer.md): Curiosity-loop narrative structures.
- [`references/character-sheets.md`](references/character-sheets.md): Multi-angle turnaround consistency specs.
- [`references/voices.md`](references/voices.md): Voice cloning parameters.
- [`references/models-and-gotchas.md`](references/models-and-gotchas.md): FFmpeg effects & API troubleshooting.
