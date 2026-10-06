# ⚡ MuAPI Integration & FFmpeg FX Recipes

This document covers technical implementation details, model endpoints, FFmpeg filter recipes, and troubleshooting gotchas for **Zack D Director**.

---

## 1. MuAPI Integration

All generation stages communicate with MuAPI through its HTTP API:

- **Text-to-Image / Reference Image Gen**: MuAPI image generation (`nano-banana-2` with `flux-dev` fallback).
- **Image-to-Video Animation**: MuAPI Veo 3.1 motion generation (`veo3.1-fast-image-to-video` with fallback).
- **Voice Cloning / TTS**: MuAPI speech generation (`minimax-speech-2.6-turbo`).
- **Music Generation**: Local or provider-generated BGM mixed during assembly.

### API Key Setup:
```bash
export MUAPI_API_KEY="sk-..."
```

---

## 2. FFmpeg Editing Effects

Zack D Director post-processing (`scripts/assemble.py`) uses short crossfades
between shots and a subtle center crop on marked impact shots. The default
transition sequence is `fade → wipeleft → slideleft → circleopen`, then it
repeats for longer projects. Use `--transition-duration 0` for hard cuts.

### A. Basic Shot Transitions

The assembler uses FFmpeg's `xfade` filter for video and `acrossfade` for audio:

```bash
python3 scripts/assemble.py out/test_run --transition-duration 0.35
```

The transition length is intentionally short so narration and beat timing stay
clear. Clips without an audio stream receive a silent fallback track.

### B. Dynamic Zoom-In on Key Impact Beats

To zoom into the subject during high-impact narration moments:
```bash
ffmpeg -i input.mp4 -vf "scale=756:1344,crop=720:1280:(iw-720)/2:(ih-1280)/2" -c:v libx264 output_zoom.mp4
```

### C. Optional Screen Shake Recipe

To simulate dramatic screen vibration during cutaways or impacts:
```bash
ffmpeg -i input.mp4 -vf "crop=in_w-20:in_h-20:10+10*sin(n*1.5):10+10*cos(n*1.5),scale=1080:1920" -c:v libx264 output_shake.mp4
```

### D. Automatic Music Ducking under Narration
```bash
ffmpeg -i narration.wav -i bgm.mp3 -filter_complex "[1:a]volume=0.15[bgm];[0:a][bgm]amix=inputs=2:duration=first[aout]" -map 0:v? -map "[aout]" final_mix.mp4
```

---

## 3. Quick Troubleshooting & Gotchas

1. **Claude / Agent can't generate images or audio**:
   - *Cause*: `MUAPI_API_KEY` is not exported or the MuAPI endpoint is unavailable.
   - *Fix*: Confirm the key is present with `export MUAPI_API_KEY="sk_..."` and retry the request.

2. **Character appearance drifts across shots**:
   - *Cause*: Keyframe generator failed to load character reference sheet.
   - *Fix*: Ensure `character_sheets.py` completed and `character_refs` array in `beats.json` points to valid turnaround files.

3. **Narration audio sounds robot-like**:
   - *Cause*: Source voice audio sample was noisy or under 30 seconds.
   - *Fix*: Re-record voice sample in a quiet room, speaking clearly for 60 seconds.
