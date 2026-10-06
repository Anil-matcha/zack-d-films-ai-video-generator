# Nano Banana 2.1 API on MuAPI

Generate and edit images with Google's Nano Banana 2.1 through one REST API. This repository is a developer guide with runnable examples for the Nano Banana 2.1 text-to-image and image-edit endpoints on MuAPI. It is an independent integration guide and is not an official Google project.

- **MuAPI:** https://muapi.ai
- **Nano Banana 2.1 API page (endpoints, comparison, FAQ):** https://muapi.ai/nano-banana-2.1
- **Text to image playground:** https://muapi.ai/playground/nano-banana-2-1
- **Image edit playground:** https://muapi.ai/playground/nano-banana-2-1-edit
- **All Nano Banana endpoints:** https://muapi.ai/nano-banana-api
- **Create/manage an API key:** https://muapi.ai/access-keys
- **API introduction:** https://muapi.ai/docs/introduction
- **Pricing:** https://muapi.ai/pricing

## Related Projects

- [MuAPI](https://muapi.ai) — Unified API for image, video, and audio generation across hundreds of AI models.
- [Nano Banana 2.1 on MuAPI](https://muapi.ai/nano-banana-2.1) — Landing page, endpoint comparison, and FAQ for this repository's API.
- [Open Generative AI](https://github.com/Anil-matcha/Open-Generative-AI) — Open-source generative-media app and model references.
- [Nano Banana Generator](https://github.com/SamurAIGPT/nano-banana-generator) — Open-source Next.js app for Nano Banana text-to-image and editing.
- [Awesome AI Image Models](https://github.com/Anil-matcha/awesome-ai-image-models) — Image model and API comparison hub.
- [Google Gemini Media API](https://github.com/Anil-matcha/Google-Gemini-Media-API) — Image and video generation API examples across Google models.
- [Qwen Image API](https://github.com/Anil-matcha/Qwen-Image-API) — Another image generation and editing API guide on the same MuAPI task API.

## What Nano Banana 2.1 is

Nano Banana 2.1 is Google's image generation and editing model on the Flash tier, the successor to Nano Banana 2 and Nano Banana Pro. It accepts text and image inputs and returns images, with 1K, 2K, and 4K output and a wide range of aspect ratios. Google describes improvements over its earlier models in visual design, mask-based editing, and subject consistency ([announcement](https://x.com/Google/status/2107501209154204148)).

On MuAPI it is exposed as two endpoints that share the same authentication, task lifecycle, and result polling as every other model.

## Choose an endpoint

| Workflow | Endpoint | What it does | Required input |
|---|---|---|---|
| Text to image | `nano-banana-2-1` | Generate an image from a prompt | `prompt` |
| Image edit | `nano-banana-2-1-edit` | Edit or combine reference images with a plain-language instruction | `prompt`, `images_list` |

Want to compare against the earlier models first? They use the same request shape:

| Model | Endpoint | Tier | Best for |
|---|---|---|---|
| Nano Banana 2.1 | `nano-banana-2-1` / `nano-banana-2-1-edit` | Flash | Latest Flash-tier generation and editing |
| Nano Banana 2 | `nano-banana-2` / `nano-banana-2-edit` | Flash | Established default |
| Nano Banana Pro | `nano-banana-pro` / `nano-banana-pro-edit` | Pro | Highest-fidelity professional work |

Check [muapi.ai/pricing](https://muapi.ai/pricing) and the model playground for current pricing and availability before production use. Prices are intentionally not copied into this README so it cannot go stale.

## How the API works

1. Submit `POST https://api.muapi.ai/api/v1/{endpoint}` with an `x-api-key` header and a JSON body.
2. Read the returned `request_id` (it is like a receipt for your image).
3. Poll `GET https://api.muapi.ai/api/v1/predictions/{request_id}/result` until the status is `completed`, then read the image URL from the result.

## Quick start: generate an image

```bash
export MUAPI_KEY="your_muapi_api_key"

curl -X POST "https://api.muapi.ai/api/v1/nano-banana-2-1" \
  -H "x-api-key: $MUAPI_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A ceramic tea set on a sunlit kitchen table, soft morning light",
    "aspect_ratio": "1:1",
    "resolution": "2k",
    "output_format": "png"
  }'
```

Then fetch the result with the returned `request_id`:

```bash
curl "https://api.muapi.ai/api/v1/predictions/REQUEST_ID/result" \
  -H "x-api-key: $MUAPI_KEY"
```

## Image edit example

`images_list` is a list of publicly reachable image URLs (the API receives URLs; it does not upload local files). Image order matters when the prompt refers to the first or second image.

```bash
curl -X POST "https://api.muapi.ai/api/v1/nano-banana-2-1-edit" \
  -H "x-api-key: $MUAPI_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Change the jacket to a teal windbreaker and keep everything else the same",
    "images_list": ["https://example.com/photo.jpg"],
    "resolution": "2k"
  }'
```

## Python example

Requires Python 3.9+ and `requests`. The script submits a generate or edit request and polls until the image is ready.

```bash
python -m pip install -r requirements.txt
export MUAPI_KEY="your_muapi_api_key"

python examples/nano_banana_21.py --prompt "A tiny greenhouse on a rainy city rooftop at dusk"

python examples/nano_banana_21.py --mode edit \
  --prompt "Turn the product into a brushed aluminum desk lamp; keep the composition" \
  --image-url "https://example.com/product.jpg"
```

## JavaScript example

Requires Node 18+ (built-in `fetch`). See [`examples/nano_banana_21.mjs`](examples/nano_banana_21.mjs).

```bash
export MUAPI_KEY="your_muapi_api_key"
node examples/nano_banana_21.mjs "A tiny greenhouse on a rainy city rooftop at dusk"
```

## Request fields

These follow the Nano Banana family contract on MuAPI. Confirm the current form for 2.1 in the [playground](https://muapi.ai/playground/nano-banana-2-1) before relying on a field.

| Field | Type | Required | Accepted values / behavior |
|---|---|---:|---|
| `prompt` | string | yes | What to generate, or the edit instruction |
| `images_list` | array of URLs | edit only | Reference images for the edit endpoint |
| `aspect_ratio` | string | no | `1:1`, `1:4`, `1:8`, `2:3`, `3:2`, `3:4`, `4:1`, `4:3`, `4:5`, `5:4`, `8:1`, `9:16`, `16:9`, `21:9`, or `Auto` |
| `resolution` | string | no | `1k`, `2k`, or `4k` (lowercase) |
| `output_format` | string | no | `jpg` or `png` |
| `google_search` | boolean | no | Use Google Search to enhance the prompt |

## Scope and honesty notes

- This repository documents how to call the endpoints through MuAPI. It does not host or modify the model.
- Model capabilities described here come from Google's public announcement; MuAPI makes no benchmark claims in this guide. Compare outputs on your own prompts in the playground.
- Endpoint availability and inputs can change; the [MuAPI Nano Banana 2.1 page](https://muapi.ai/nano-banana-2.1) is the source of truth.

## License

MIT, see [LICENSE](LICENSE).
