# 🎙️ Voice Cloning & Narration Setup

A signature element of Zack D Films shorts is the fast, energetic, clear narration.

---

## 1. Voice Recording Requirements

To clone your voice for Zack D Director shorts:
1. **Duration**: Record **~60 seconds** of clean audio.
2. **Environment**: Quiet room, minimal echo, no background music or noise.
3. **Tone & Pace**: Speak at a natural, slightly enthusiastic, articulate pace (approx. 150–175 words per minute).
4. **Format**: Save as `.mp3` or `.wav` (e.g. `my_voice_sample.mp3`).

---

## 2. Voice Synthesis Parameters

When running `scripts/audio.py`, the script sends the prompt and voice sample to the configured TTS engine:

```bash
python scripts/audio.py out/<project> --voice-sample voice_recording.mp3
```

- **Speed / Pacing**: `1.1x` speed modifier for energetic viral short pacing.
- **Audio Ducking**: Background music (BGM) is ducked down by **-18dB** automatically whenever narration audio plays.
- **Audio Equalization**: Speech filter applied via FFmpeg (`highpass=f=80, lowpass=f=8000, volume=1.2`) for studio warmth.
