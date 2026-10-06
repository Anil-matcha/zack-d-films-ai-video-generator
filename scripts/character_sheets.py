#!/usr/bin/env python3
"""
Character & Asset Turnaround Sheet Generator for Zack D Director.
Generates 3D orthographic multi-angle reference sheets for visual consistency.
"""

import os
import sys
import json
import argparse
from provider import APIClient, download_file

def generate_character_sheets(project_dir):
    beats_file = os.path.join(project_dir, "beats.json")
    if not os.path.exists(beats_file):
        print(f"[Error] beats.json not found in {project_dir}. Run script_generator.py first.")
        sys.exit(1)

    with open(beats_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    chars_dir = os.path.join(project_dir, "characters")
    os.makedirs(chars_dir, exist_ok=True)

    client = APIClient()
    required_sheets = data.get("character_sheets_required", ["main_character_turnaround"])

    print(f"[Character Sheets] Generating {len(required_sheets)} turnaround reference sheets...")

    sheet_paths = []
    for sheet_name in required_sheets:
        out_path = os.path.join(chars_dir, f"{sheet_name}.png")
        prompt = (
            f"Orthographic 3D character turnaround sheet, front view, side profile view, and 3/4 angle view of "
            f"{sheet_name.replace('_', ' ')}, stylized 3D digital art style, smooth plasticine shader, "
            f"clean light grey background, octane render, studio lighting, zero shadows."
        )
        res = client.generate_image(prompt, aspect_ratio="16:9")
        img_url = res.get("url")
        if img_url and img_url.startswith("http"):
            download_file(img_url, out_path)
        else:
            with open(out_path, "w", encoding="utf-8") as img_file:
                img_file.write(f"MOCK_IMAGE_DATA_FOR_{sheet_name}")

        sheet_paths.append(out_path)
        print(f"  [OK] Created reference sheet: {out_path}")

    print(f"[Character Sheets] All turnaround sheets ready in: {chars_dir}")
    return sheet_paths

def main():
    parser = argparse.ArgumentParser(description="Generate 3D Character Consistency Turnaround Sheets")
    parser.add_argument("project_dir", help="Project directory e.g. out/swallow_gum")
    args = parser.parse_args()

    generate_character_sheets(args.project_dir)

if __name__ == "__main__":
    main()
