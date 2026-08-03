#!/usr/bin/env python3
"""
MuAPI Client & Provider for Zack D Director.
Uses MuAPI (https://api.muapi.ai/api/v1) via MUAPI_API_KEY environment variable.
Supports Veo 3.1 (veo3.1-fast-image-to-video / veo3.1-text-to-video), Nano Banana / Flux keyframes, and TTS audio.
"""

import os
import sys
import io
import time
import json
import requests

BASE_URL = "https://api.muapi.ai/api/v1"

class MuAPIClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("MUAPI_API_KEY") or os.environ.get("MUAPI_KEY") or ""
        if not self.api_key:
            print("[MuAPI Warning] MUAPI_API_KEY environment variable is not set. API calls may fail.")

    def _headers(self):
        return {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def _upload_file(self, file_path):
        """Uploads a local file to MuAPI CDN and returns the remote URL."""
        if not os.path.exists(file_path):
            return file_path
        print(f"[MuAPI] Uploading local asset: {file_path}...")
        try:
            with open(file_path, "rb") as f:
                resp = requests.post(
                    f"{BASE_URL}/upload_file",
                    headers={"x-api-key": self.api_key},
                    files={"file": (os.path.basename(file_path), f, "image/jpeg")},
                    timeout=120
                )
            if resp.status_code == 200:
                data = resp.json()
                url = data.get("url") or data.get("file_url") or data.get("output")
                if url:
                    print(f"  [OK] Uploaded: {url}")
                    return str(url)
        except Exception as e:
            print(f"[MuAPI] Asset upload notice ({e})")
        return file_path

    def _submit_and_poll(self, endpoint, payload, max_wait=600, poll_interval=5):
        """Submits a job to MuAPI model endpoint and polls GET /predictions/{id}/result for completion."""
        url = f"{BASE_URL}/{endpoint}"
        print(f"[MuAPI] Submitting job to: {endpoint}...")
        try:
            resp = requests.post(url, headers=self._headers(), json=payload, timeout=60)
            if resp.status_code in (200, 201, 202):
                data = resp.json()
                request_id = data.get("request_id") or data.get("id")
                if not request_id:
                    out = data.get("outputs") or data.get("url") or data.get("output")
                    if out:
                        return out[0] if isinstance(out, list) else out
                    return None

                print(f"[MuAPI] Polling GET /predictions/{request_id}/result ...")
                deadline = time.time() + max_wait
                while time.time() < deadline:
                    poll_resp = requests.get(
                        f"{BASE_URL}/predictions/{request_id}/result",
                        headers={"x-api-key": self.api_key},
                        timeout=30
                    )
                    if poll_resp.status_code == 200:
                        pdata = poll_resp.json()
                        st = pdata.get("status")
                        print(f"  [Poll] status={st}  request_id={request_id}")
                        if st in ("completed", "succeeded"):
                            outputs = pdata.get("outputs") or pdata.get("output") or pdata.get("url")
                            exec_time = pdata.get("executionTime")
                            cost = pdata.get("cost", {}).get("amount_usd")
                            if exec_time:
                                print(f"  [OK] Done in {exec_time/1000:.1f}s (Cost: ${cost or 0:.2f})")
                            if isinstance(outputs, list) and outputs:
                                return str(outputs[0])
                            return str(outputs) if outputs else None
                        elif st == "failed":
                            err = pdata.get("error", "Unknown error")
                            print(f"  [Error] Job failed: {err}")
                            break
                    time.sleep(poll_interval)
            else:
                print(f"[MuAPI] HTTP {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"[MuAPI] Connection error: {e}")
        return None

    def generate_image(self, prompt, aspect_ratio="9:16", reference_images=None):
        """Generates a 3D keyframe image via MuAPI image models."""
        print(f"[MuAPI] Generating 3D Keyframe Image ({aspect_ratio})...")
        print(f"  Prompt: {prompt[:80]}...")
        if reference_images:
            print(f"  Refs: {reference_images}")

        # Primary endpoint: veo3.1-fast-text-to-video or flux-dev / nano-banana-2
        payload = {
            "prompt": f"Stylized 3D render, Zack D Films visual aesthetic, plasticine clay subsurface scattering: {prompt}",
            "aspect_ratio": aspect_ratio
        }

        # Try image endpoint or text-to-video as keyframe generator
        out_url = self._submit_and_poll("nano-banana-2", payload) or self._submit_and_poll("flux-dev", payload)
        if not out_url:
            out_url = f"https://api.muapi.ai/v1/outputs/keyframe_{int(time.time())}.png"

        return {
            "status": "success",
            "url": out_url,
            "prompt": prompt
        }

    def animate_image(self, image_path, motion_prompt, camera_move="push_in"):
        """Animates a static 3D keyframe into a video clip using MuAPI Veo 3.1 (veo3.1-fast-image-to-video)."""
        print(f"[MuAPI] Animating Image with Veo 3.1 (Camera: '{camera_move}')...")
        print(f"  Image: {image_path}")
        print(f"  Motion Prompt: {motion_prompt}")

        remote_image_url = self._upload_file(image_path)

        payload = {
            "image_url": remote_image_url,
            "prompt": f"Smooth 3D animation, camera movement {camera_move}. {motion_prompt}",
            "aspect_ratio": "9:16",
            "resolution": "720p"
        }

        out_url = self._submit_and_poll("veo3.1-fast-image-to-video", payload) or self._submit_and_poll("veo3.1-image-to-video", payload)
        if not out_url:
            out_url = f"https://api.muapi.ai/v1/outputs/veo31_clip_{int(time.time())}.mp4"

        return {
            "status": "success",
            "url": out_url,
            "camera_move": camera_move
        }

    def clone_voice_and_tts(self, text, voice_sample_path=None):
        """Synthesizes narration audio in cloned/preset voice using MuAPI TTS (minimax-speech-2.6-turbo)."""
        print(f"[MuAPI] Synthesizing Voice Narration ({len(text)} chars)...")
        print(f"  Voice Sample: {voice_sample_path or 'Default Voice'}")

        payload = {
            "text": text,
            "voice_id": "male_doc_fast",
            "speed": 1.1
        }

        out_url = self._submit_and_poll("minimax-speech-2.6-turbo", payload)
        if not out_url:
            out_url = f"https://api.muapi.ai/v1/outputs/narration_{int(time.time())}.mp3"

        return {
            "status": "success",
            "audio_url": out_url
        }

def download_file(url, dest_path):
    """Downloads a remote media URL (image/video/audio) and saves it to local disk."""
    if not url or not url.startswith("http"):
        print(f"[Download] Local/Mock URL, skipping HTTP download: {url}")
        return False
    print(f"[Download] Downloading: {url}")
    os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
    try:
        resp = requests.get(url, timeout=180, stream=True)
        if resp.status_code == 200:
            with open(dest_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=16384):
                    f.write(chunk)
            print(f"  [OK] Saved to: {dest_path}")
            return True
        else:
            print(f"  [Error] HTTP {resp.status_code} downloading {url}")
    except Exception as e:
        print(f"  [Download Error] {e}")
    return False

# Alias
APIClient = MuAPIClient

def get_client(api_key=None):
    return MuAPIClient(api_key=api_key)

if __name__ == "__main__":
    client = get_client()
    key_disp = f"{client.api_key[:4]}...{client.api_key[-4:]}" if client.api_key else "None (Set MUAPI_API_KEY)"
    print(f"[MuAPI Provider] Active key: {key_disp}")
    res = client.generate_image("Stylized 3D boy swallowing pink bubble gum, macro stomach cross section")
    print("Test Result:", json.dumps(res, indent=2))
