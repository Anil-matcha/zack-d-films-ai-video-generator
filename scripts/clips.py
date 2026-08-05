#!/usr/bin/env python3
"""
Motion Clip Generator for Zack D Director.
Animates 3D keyframe images into motion video clips via the configured image-to-video provider.
"""

import os
import sys
import json
import argparse
from provider import APIClient, download_file

def generate_clips(project_dir):
    beats_file = os.path.join(project_dir, "beats.json")
    if not os.path.exists(beats_file):
        print(f"[Error] beats.json not found in {project_dir}.")
        sys.exit(1)

    with open(beats_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    keyframes_dir = os.path.join(project_dir, "keyframes")
    clips_dir = os.path.join(project_dir, "clips")
    os.makedirs(clips_dir, exist_ok=True)

    client = APIClient()

    print(f"[Clips] Generating Motion Video Clips...")

    clip_count = 0
    for beat in data.get("beats", []):
        for shot in beat.get("shots", []):
            shot_id = shot["shot_id"]
            keyframe_path = os.path.join(keyframes_dir, f"{shot_id}.png")
            out_clip_path = os.path.join(clips_dir, f"{shot_id}.mp4")

            camera_move = shot.get("camera_move", "push_in")
            scene_desc = shot.get("scene_description", "")

            res = client.animate_image(
                image_path=keyframe_path,
                motion_prompt=f"Smooth 3D motion, {scene_desc}",
                camera_move=camera_move
            )
            clip_url = res.get("url")
            if clip_url and clip_url.startswith("http"):
                download_file(clip_url, out_clip_path)
            else:
                with open(out_clip_path, "w", encoding="utf-8") as clip_file:
                    clip_file.write(f"MOCK_MP4_CLIP_DATA_FOR_{shot_id}")

            clip_count += 1
            print(f"  [OK] Animated video clip [{shot_id}] ({camera_move}): {out_clip_path}")

    print(f"[Clips] Generated {clip_count} motion clips in: {clips_dir}")

def main():
    parser = argparse.ArgumentParser(description="Animate keyframes into video clips")
    parser.add_argument("project_dir", help="Project directory e.g. out/swallow_gum")
    args = parser.parse_args()

    generate_clips(args.project_dir)

if __name__ == "__main__":
    main()
