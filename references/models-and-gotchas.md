# ⚡ Higgsfield API / MCP Integration & FFmpeg FX Recipes

This document covers technical implementation details, model endpoints, FFmpeg filter recipes, and troubleshooting gotchas for **Zack D Director**.

---

## 1. Higgsfield MCP & API Integration

All generation stages communicate with Higgsfield via the MCP Connector or HTTP API:

- **Text-to-Image / Reference Image Gen**: `higgsfield/3d-stylized-v1` (or Nano Banana 3D preset).
- **Image-to-Video Animation**: `higgsfield/i2v-camera-v2` (supports push-in, tilt, pan, and orbital moves).
- **Voice Cloning / TTS**: `higgsfield/voice-clone-v1`.
- **Music Generation**: `higgsfield/bgm-synth-v1`.

### API Key Setup:
```bash
export HIGGSFIELD_API_KEY="sk_higgsfield_..."
```

---

## 2. FFmpeg Editing Effects Recipes

Zack D Director post-processing (`scripts/assemble.py`) uses two custom FFmpeg filters for visual pop:

### A. Dynamic Zoom-In on Key Impact Beats (`zoompan`)
To zoom into the subject during high-impact narration moments:
```bash
ffmpeg -i input.mp4 -vf "zoompan=z='min(zoom+0.003,1.25)':d=90:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920" -c:v libx264 output_zoom.mp4
```

### B. Screen Shake on Scene Transitions (`crop + noise`)
To simulate dramatic screen vibration during cutaways or impacts:
```bash
ffmpeg -i input.mp4 -vf "crop=in_w-20:in_h-20:10+10*sin(n*1.5):10+10*cos(n*1.5),scale=1080:1920" -c:v libx264 output_shake.mp4
```

### C. Automatic Music Ducking under Narration
```bash
ffmpeg -i narration.wav -i bgm.mp3 -filter_complex "[1:a]volume=0.15[bgm];[0:a][bgm]amix=inputs=2:duration=first[aout]" -map 0:v? -map "[aout]" final_mix.mp4
```

---

## 3. Quick Troubleshooting & Gotchas

1. **Claude / Agent can't generate images or audio**:
   - *Cause*: MCP Connector is inactive or `HIGGSFIELD_API_KEY` is not exported.
   - *Fix*: Re-add custom connector in Claude settings or run `export HIGGSFIELD_API_KEY="sk_..."`.

2. **Character appearance drifts across shots**:
   - *Cause*: Keyframe generator failed to load character reference sheet.
   - *Fix*: Ensure `character_sheets.py` completed and `character_refs` array in `beats.json` points to valid turnaround files.

3. **Narration audio sounds robot-like**:
   - *Cause*: Source voice audio sample was noisy or under 30 seconds.
   - *Fix*: Re-record voice sample in a quiet room, speaking clearly for 60 seconds.
