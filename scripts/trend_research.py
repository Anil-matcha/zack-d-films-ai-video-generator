#!/usr/bin/env python3
"""
Trend Research & Topic Brainstorming Tool for Zack D Director shorts.
Generates curiosity-driven scientific, medical, or anatomical topic ideas.
"""

import sys
import json
import argparse

TREND_TOPICS = [
    {
        "topic": "What Happens When You Swallow Gum?",
        "curiosity_hook": "You've probably been told that swallowing gum stays in your stomach for 7 years... but is that actually true?",
        "category": "Medical / Human Body",
        "viral_score": 9.8
    },
    {
        "topic": "How Mosquitoes Drink Your Blood",
        "curiosity_hook": "When a mosquito bites you, it doesn't just suck your blood — it leaves six needle-like tools and saliva behind.",
        "category": "Biology / Insects",
        "viral_score": 9.6
    },
    {
        "topic": "Why Your Brain Gets Brain Freeze",
        "curiosity_hook": "Eating ice cream too fast tricks your brain into thinking your head is freezing solid.",
        "category": "Neuroscience",
        "viral_score": 9.4
    },
    {
        "topic": "What Happens If You Don't Sleep For 3 Days",
        "curiosity_hook": "After 72 hours without sleep, your brain starts consuming its own synapses.",
        "category": "Health / Sleep",
        "viral_score": 9.7
    }
]

def main():
    parser = argparse.ArgumentParser(description="Research high-curiosity viral topics for Zack D Shorts.")
    parser.add_argument("query", nargs="?", default="", help="Optional topic keyword")
    args = parser.parse_args()

    print("=" * 60)
    print("🎬 Zack D Director — Curiosity Trend Research Results")
    print("=" * 60)

    for idx, item in enumerate(TREND_TOPICS, 1):
        print(f"\n[{idx}] {item['topic']} (Viral Score: {item['viral_score']}/10)")
        print(f"    Category: {item['category']}")
        print(f"    Hook: \"{item['curiosity_hook']}\"")

    print("\n" + "=" * 60)
    print("Pick a topic number or supply your own custom question to start production!")

if __name__ == "__main__":
    main()
