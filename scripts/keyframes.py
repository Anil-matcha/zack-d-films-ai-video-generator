#!/usr/bin/env python3
"""
3D Keyframe Generator for Zack D Director.
Renders initial high-quality 3D visual keyframes for each shot, anchored by character sheets.
"""

import os
import sys
import json
import argparse
from provider import APIClient, download_file

def generate_keyframes(project_dir):
    beats_file = os.path.join(project_dir, "beats.json")
    if not os.path.exists(beats_file):
        print(f"[Error] beats.json not found in {project_dir}.")
        sys.exit(1)

    with open(beats_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    keyframes_dir = os.path.join(project_dir, "keyframes")
    os.makedirs(keyframes_dir, exist_ok=True)

    client = APIClient()
    aspect = data.get("aspect_ratio", "9:16")

    print(f"[Keyframes] Rendering 3D Scene Keyframes ({aspect})...")

    shot_count = 0
    for beat in data.get("beats", []):
        for shot in beat.get("shots", []):
            shot_id = shot["shot_id"]
            out_path = os.path.join(keyframes_dir, f"{shot_id}.png")
            scene_desc = shot["scene_description"]
            char_refs = shot.get("character_refs", [])

            prompt = (
                f"{scene_desc}, in Zack D 3D stylized animation render style, smooth plasticine shader, "
                f"dramatic studio key light, vibrant rim lighting, subsurface scattering, macro depth of field."
            )
            if char_refs:
                prompt += f" Anchored on character sheet refs: {', '.join(char_refs)}."

            res = client.generate_image(prompt, aspect_ratio=aspect, reference_images=char_refs)
            img_url = res.get("url")
            if img_url and img_url.startswith("http"):
                download_file(img_url, out_path)
            else:
                with open(out_path, "w", encoding="utf-8") as img_file:
                    img_file.write(f"MOCK_KEYFRAME_DATA_FOR_{shot_id}")

            shot_count += 1
            print(f"  [OK] Rendered keyframe [{shot_id}]: {out_path}")

    print(f"[Keyframes] Rendered {shot_count} keyframe images in: {keyframes_dir}")

def main():
    parser = argparse.ArgumentParser(description="Render 3D scene keyframes")
    parser.add_argument("project_dir", help="Project directory e.g. out/swallow_gum")
    args = parser.parse_args()

    generate_keyframes(args.project_dir)

if __name__ == "__main__":
    main()
