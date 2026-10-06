#!/usr/bin/env python3
"""
Script Generator & Beat Breakdown Tool for Zack D Director.
Generates structured curiosity-loop beats.json for project folders.
"""

import os
import sys
import json
import argparse

def generate_script(project_dir, topic):
    os.makedirs(project_dir, exist_ok=True)
    beats_file = os.path.join(project_dir, "beats.json")

    # Clean project name from path
    proj_name = os.path.basename(os.path.normpath(project_dir))

    beats_data = {
        "project_name": proj_name,
        "topic": topic,
        "aspect_ratio": "9:16",
        "style_preset": "zackd_3d_stylized",
        "narrator_voice": "cloned_user_voice",
        "character_sheets_required": [
            "main_character_turnaround",
            "anatomical_organ_cross_section"
        ],
        "beats": [
            {
                "beat_id": "beat_1",
                "narration": f"{topic} Here is what actually happens inside your body.",
                "title_cn": "开场钩子",
                "title_en": "Curiosity Hook",
                "hook": True,
                "shots": [
                    {
                        "shot_id": "beat_1_a",
                        "type": "wide",
                        "duration_sec": 3.0,
                        "scene_description": f"Stylized 3D main character experiencing {topic}, wide shot in bright studio lighting.",
                        "camera_move": "push_in",
                        "character_refs": ["main_character_turnaround"],
                        "zoom_impact": False
                    },
                    {
                        "shot_id": "beat_1_b",
                        "type": "macro_cross_section",
                        "duration_sec": 3.0,
                        "scene_description": f"Detailed anatomical 3D cutaway cross-section illustrating {topic} mechanism.",
                        "camera_move": "tilt_down",
                        "character_refs": ["anatomical_organ_cross_section"],
                        "zoom_impact": True
                    }
                ]
            },
            {
                "beat_id": "beat_2",
                "narration": "Your bodily defenses immediately kick in, attempting to neutralize the situation.",
                "title_cn": "身体机制",
                "title_en": "Biological Reaction",
                "hook": False,
                "shots": [
                    {
                        "shot_id": "beat_2_a",
                        "type": "macro",
                        "duration_sec": 3.0,
                        "scene_description": "Microscopic view of fluids and enzymes interacting with the object in 3D clay style.",
                        "camera_move": "pan_right",
                        "character_refs": ["anatomical_organ_cross_section"],
                        "zoom_impact": False
                    },
                    {
                        "shot_id": "beat_2_b",
                        "type": "detail",
                        "duration_sec": 3.0,
                        "scene_description": "Close up of muscular contractions pushing the subject through the digestive tract.",
                        "camera_move": "static",
                        "character_refs": ["anatomical_organ_cross_section"],
                        "zoom_impact": True
                    }
                ]
            },
            {
                "beat_id": "beat_3",
                "narration": "In the end, your body safely processes it and flushes it out within just a couple of days!",
                "title_cn": "结局破局",
                "title_en": "The Resolution",
                "hook": False,
                "shots": [
                    {
                        "shot_id": "beat_3_a",
                        "type": "wide",
                        "duration_sec": 3.0,
                        "scene_description": "Stylized 3D main character smiling in relief, bright vibrant lighting, success emote.",
                        "camera_move": "pull_out",
                        "character_refs": ["main_character_turnaround"],
                        "zoom_impact": False
                    }
                ]
            }
        ]
    }

    with open(beats_file, "w", encoding="utf-8") as f:
        json.dump(beats_data, f, indent=2, ensure_ascii=False)

    print(f"[Script Generator] Created curiosity beats breakdown at: {beats_file}")
    return beats_data

def main():
    parser = argparse.ArgumentParser(description="Generate curiosity loop beats.json")
    parser.add_argument("project_dir", help="Output project directory e.g. out/swallow_gum")
    parser.add_argument("--topic", default="What Happens When You Swallow Gum?", help="Topic question")
    parser.add_argument("--dry-run", action="store_true", help="Print breakdown without saving")

    args = parser.parse_args()

    if args.dry_run:
        print(f"[Dry Run] Script breakdown for topic: '{args.topic}'")
    else:
        generate_script(args.project_dir, args.topic)

if __name__ == "__main__":
    main()
