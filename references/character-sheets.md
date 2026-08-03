# 🧍 Character & Asset Consistency Sheets System

Maintaining exact visual identity across multiple 3D generated scenes is the single biggest technical challenge in AI video generation.

**Zack D Director** solves this with the **Character Sheet Backbone Method**:

---

## 1. The Character Sheet Concept

Before rendering any scene in the video, the pipeline generates an **orthographic turnaround sheet** (front view, side view, 3/4 view, back view) on a clean light studio background for every recurring character, organ, or main object.

```
+-----------------------------------------------------------------------+
|                       CHARACTER TURNAROUND SHEET                     |
|                                                                       |
|  [ FRONT VIEW ]      [ 3/4 ANGLE VIEW ]      [ SIDE PROFILE VIEW ]     |
|                                                                       |
|  Stylized 3D Boy     Stylized 3D Boy         Stylized 3D Boy          |
|  Blue T-shirt        Blue T-shirt            Blue T-shirt             |
|  Brown Hair          Brown Hair              Brown Hair               |
+-----------------------------------------------------------------------+
```

---

## 2. Generating Character Sheets

Run `scripts/character_sheets.py` to generate turnaround sheets for a project:

```bash
python scripts/character_sheets.py out/<project>
```

### Prompt Template for Character Turnaround:
> `Orthographic 3D character turnaround sheet, front view, side profile view, and 3/4 angle view of a [SUBJECT DESCRIPTION], stylized 3D digital art style, smooth plasticine shader, clean light grey background, octane render, studio lighting, zero shadows.`

### Prompt Template for Anatomical / Asset Turnaround:
> `3D medical model turnaround sheet, front view and cross-section cutaway view of [HUMAN ORGAN / ASSET DESCRIPTION], semi-translucent glossy tissue, bright interior lighting, clean background, high contrast specular highlights.`

---

## 3. Feeding Sheets into Scene Keyframes

When `scripts/keyframes.py` renders scene keyframes, it references the character sheet as an **Image-to-Image / Control reference seed** or explicitly embeds the character sheet's feature description:

```python
# Example logic in keyframes.py
prompt = f"Using character reference {sheet_path}: {scene_description}, in Zack D 3D render style..."
```

This guarantees that:
- The character's hair color, facial structure, shirt color, and body shape stay identical across all camera angles.
- Organs, stomach acid color, and anatomical details remain uniform throughout the short.
