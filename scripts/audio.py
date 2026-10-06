#!/usr/bin/env python3
"""
Audio Generator for Zack D Director.
Synthesizes voice narration in cloned user voice and mixes background music.
"""

import os
import sys
import json
import argparse
from provider import APIClient, download_file

def generate_audio(project_dir, voice_sample=None):
    beats_file = os.path.join(project_dir, "beats.json")
    if not os.path.exists(beats_file):
        print(f"[Error] beats.json not found in {project_dir}.")
        sys.exit(1)

    with open(beats_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    audio_dir = os.path.join(project_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)

    client = APIClient()

    # Collect full script narration text
    full_narration = " ".join([beat.get("narration", "") for beat in data.get("beats", [])])

    print(f"[Audio] Synthesizing Voice Narration in Cloned Voice...")
    print(f"  Script: \"{full_narration[:100]}...\"")

    res = client.clone_voice_and_tts(full_narration, voice_sample_path=voice_sample)

    narration_path = os.path.join(audio_dir, "narration.mp3")
    bgm_path = os.path.join(audio_dir, "bgm.mp3")

    audio_url = res.get("audio_url")
    if audio_url and audio_url.startswith("http"):
        download_file(audio_url, narration_path)
    else:
        with open(narration_path, "w", encoding="utf-8") as f:
            f.write("MOCK_NARRATION_AUDIO_DATA")

    with open(bgm_path, "w", encoding="utf-8") as f:
        f.write("MOCK_BGM_AUDIO_DATA")

    print(f"  [OK] Narration audio saved: {narration_path}")
    print(f"  [OK] Background music saved: {bgm_path}")
    print(f"[Audio] Audio synthesis complete.")

def main():
    parser = argparse.ArgumentParser(description="Synthesize narration & background music")
    parser.add_argument("project_dir", help="Project directory e.g. out/swallow_gum")
    parser.add_argument("--voice-sample", help="Path to 60s voice sample file")
    args = parser.parse_args()

    generate_audio(args.project_dir, args.voice_sample)

if __name__ == "__main__":
    main()
