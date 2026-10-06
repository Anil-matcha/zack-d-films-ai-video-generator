# 🎨 Zack D Films 3D Visual Style & Prompt Engineering Guide

This guide defines the precise 3D rendering art direction, visual prompt structures, materials, lighting, and camera styles required to replicate the iconic **Zack D Films** look.

---

## 1. Core Visual Aesthetic Pillars

The Zack D Films visual language combines **stylized 3D digital art**, **anatomical precision**, and **dramatic studio lighting**:

1. **Stylized 3D Character Models**: Smooth, slightly exaggerated human features with clean topology. 피부 and surfaces use subtle clay or plasticine subsurface scattering (SSS).
2. **Internal Anatomical Cross-Sections**: Semi-transparent, glowing, or clear cutaway views showing bodily organs (stomach, esophagus, blood vessels, brain, skin layers) or mechanical mechanisms.
3. **Dramatic High-Contrast Lighting**: Rim lighting, bright primary key light, subtle specular highlights, ambient occlusion, and dark clean background tones (dark grey, deep blue, deep red studio space).
4. **Cinematic Macro Camera**: Extreme close-up lens, shallow depth of field (bokeh background), precise focal points on key anatomical/physical interactions.

---

## 2. The 5-Part 3D Image Prompt Structure

Every image keyframe prompt **MUST** follow this 5-part template to maintain consistent aesthetic quality:

```
[SUBJECT & ACTION] + [CHARACTER / ASSET ANCHOR] + [3D ART STYLE & MATERIAL] + [LIGHTING & CAMERA] + [BACKGROUND & ATMOSPHERE]
```

### Example Prompt:
> **Subject & Action**: A sticky wad of pink chewing gum sliding slowly down a smooth pink esophageal tract into a stomach filled with yellow digestive fluid.
> **Character Anchor**: Rendered using character sheet ref `gut_cross_section_v1`.
> **3D Art Style & Material**: 3D stylized digital animation, smooth plasticine material with subtle subsurface scattering, glossy specular highlights, detailed cross-section view.
> **Lighting & Camera**: Macro 85mm lens shot, shallow depth of field, dramatic blue rim light, soft top studio key light, crisp ambient occlusion.
> **Background & Atmosphere**: Dark clean studio background, subtle ambient particles in stomach fluid.

---

## 3. Visual Keywords Roster

Include these exact keyword phrases to guarantee the signature 3D look:

- **Style**: `3d stylized animation`, `zack d films render style`, `digital 3d sculpture`, `octane render aesthetic`.
- **Shaders & Texture**: `subsurface scattering (SSS)`, `glossy plasticine texture`, `clean polymer clay shader`, `smooth polished surface`, `semi-translucent organ tissue`.
- **Lighting**: `volumetric studio lighting`, `vibrant rim light`, `high contrast specularity`, `soft ambient occlusion`, `dramatic key light`.
- **Camera & Views**: `macro cross-section cutaway view`, `anatomical cross section`, `extreme close-up 85mm lens`, `shallow depth of field`, `cinematic focus`.

---

## 4. Negative Prompts / Avoidances

Never include terms that lead to 2D art, photorealistic real humans, or messy noisy scenes:
- `photorealistic human skin, realistic face photography, 2D illustration, flat vector art, sketch, anime, low resolution, grainy texture, blurry details`.
