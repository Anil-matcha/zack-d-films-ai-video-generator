# 📖 The Curiosity-Loop Script Structure & Pacing

Zack D Films videos achieve industry-leading retention rates because of a specific scriptwriting formula known as the **Curiosity Loop**.

---

## 1. What is a Curiosity Loop?

A Curiosity Loop occurs when a script sentence opens a gap in the viewer's knowledge — a question their brain physically needs answered. Instead of giving a dry explanation, every line opens the next micro-question before answering the previous one.

### The 4 Curiosity Script Formulas:

1. **The Myth-Buster Loop**:
   - *Line 1 (Hook)*: "You've probably heard that swallowing gum stays in your stomach for 7 years... but is that actually true?"
   - *Line 2 (Mechanism)*: "When you swallow gum, your saliva tries to break it down immediately using enzymes, but fails."
   - *Line 3 (Escalation)*: "So your stomach muscles start churning it, moving it toward stomach acid powerful enough to dissolve metal."
   - *Line 4 (Twist)*: "Yet the gum base completely resists the acid. So what happens to it next?"
   - *Line 5 (Resolution/Punchline)*: "Your digestive system treats it like insoluble fiber, passing it safely through your intestine in just a few days!"

2. **The "What If" Bodily Horror Loop**:
   - *Line 1 (Hook)*: "If a mosquito bites you, it doesn't just suck your blood — it leaves something terrifying behind."
   - *Line 2*: "First, it inserts six needle-like mouthparts into your skin."
   - *Line 3*: "While one tube draws blood, another pumps saliva containing anticoagulants and local anesthetics."
   - *Line 4*: "Your immune system reacts by releasing histamine, causing the bump to swell and itch furiously!"

---

## 2. Visual Pacing & Shot Cadence

- **Shot Duration**: Every shot must run **2 to 4 seconds**. Never hold a single shot for longer than 4 seconds.
- **2 Shots per Beat**: Each script beat (5–8 seconds of narration) should be split into **2 visual shots**:
  1. **Shot A (Establishing Wide)**: Shows the main subject and action (e.g. person swallowing gum).
  2. **Shot B (Cutaway Macro / Cross-Section)**: Cuts directly into the anatomical interior (e.g. gum inside esophagus).
- **Camera Motion Variance**: Alternate camera movements across consecutive beats:
  - Beat 1: Push In (Zoom)
  - Beat 2: Pan Left-to-Right
  - Beat 3: Tilt Up/Down
  - Beat 4: Static (Impact Moment)

---

## 3. Beat Map JSON Schema (`beats.json`)

```json
{
  "project_name": "swallow_gum",
  "topic": "What Happens When You Swallow Gum?",
  "narrator_voice": "cloned_user_voice",
  "aspect_ratio": "9:16",
  "beats": [
    {
      "id": "beat_1",
      "hook": true,
      "narration": "You've probably been told that swallowing gum stays in your stomach for 7 years.",
      "title_cn": "吞口香糖的传说",
      "title_en": "Swallowing Gum Myth",
      "shots": [
        {
          "shot_id": "beat_1_a",
          "type": "wide",
          "duration_sec": 3.0,
          "scene_description": "Stylized 3D boy accidentally swallowing a large pink bubble gum, wide shot.",
          "camera_move": "push_in",
          "character_refs": ["boy_turnaround"],
          "zoom_impact": false
        },
        {
          "shot_id": "beat_1_b",
          "type": "macro_cross_section",
          "duration_sec": 3.0,
          "scene_description": "Cross section view of esophagus showing pink gum sliding down throat.",
          "camera_move": "tilt_down",
          "character_refs": ["gut_turnaround"],
          "zoom_impact": true
        }
      ]
    }
  ]
}
```
