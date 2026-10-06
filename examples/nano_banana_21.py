#!/usr/bin/env python3
"""Submit and poll a Nano Banana 2.1 image task through the MuAPI REST API."""

import argparse
import os
import sys
import time
from typing import Any

import requests

BASE_URL = "https://api.muapi.ai/api/v1"
DONE = {"completed", "succeeded", "success"}
FAILED = {"failed", "error", "cancelled", "canceled"}


def request_json(method: str, url: str, api_key: str, **kwargs: Any) -> dict[str, Any]:
    response = requests.request(
        method,
        url,
        headers={"x-api-key": api_key, "Content-Type": "application/json"},
        timeout=30,
        **kwargs,
    )
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        raise RuntimeError("API returned an unexpected non-object JSON response")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("generate", "edit"), default="generate")
    parser.add_argument("--prompt", required=True, help="Image prompt or editing instruction")
    parser.add_argument(
        "--image-url",
        action="append",
        default=[],
        help="Publicly reachable reference image URL (repeat for several; edit mode only)",
    )
    parser.add_argument("--resolution", choices=("1k", "2k", "4k"), default="1k")
    parser.add_argument("--aspect-ratio", default=None, help="For example 1:1, 16:9, 9:16 or Auto")
    parser.add_argument("--output-format", choices=("jpg", "png"), default=None)
    parser.add_argument("--timeout", type=int, default=600, help="Maximum polling time in seconds")
    parser.add_argument("--poll-interval", type=float, default=5.0, help="Polling interval in seconds")
    args = parser.parse_args()

    api_key = os.environ.get("MUAPI_KEY")
    if not api_key:
        parser.error("Set MUAPI_KEY in the environment")
    if args.mode == "edit" and not args.image_url:
        parser.error("--mode edit requires at least one --image-url")
    if args.mode == "generate" and args.image_url:
        parser.error("--image-url is only valid with --mode edit")

    endpoint = "nano-banana-2-1" if args.mode == "generate" else "nano-banana-2-1-edit"
    payload: dict[str, Any] = {"prompt": args.prompt, "resolution": args.resolution}
    if args.mode == "edit":
        payload["images_list"] = args.image_url
    if args.aspect_ratio:
        payload["aspect_ratio"] = args.aspect_ratio
    if args.output_format:
        payload["output_format"] = args.output_format

    submitted = request_json("POST", f"{BASE_URL}/{endpoint}", api_key, json=payload)
    request_id = submitted.get("request_id")
    if not request_id:
        raise RuntimeError(f"Submission response did not include request_id: {submitted}")
    print(f"Submitted request: {request_id}")

    deadline = time.monotonic() + args.timeout
    result_url = f"{BASE_URL}/predictions/{request_id}/result"
    while time.monotonic() < deadline:
        result = request_json("GET", result_url, api_key)
        status = str(result.get("status", "")).lower()
        if status in DONE:
            outputs = result.get("outputs", result.get("output", []))
            for output in outputs if isinstance(outputs, list) else [outputs]:
                print(output.get("url") if isinstance(output, dict) else output)
            return 0
        if status in FAILED:
            print(f"Task ended with status {status}: {result}", file=sys.stderr)
            return 1
        print(f"Status: {status or 'pending'}")
        time.sleep(args.poll_interval)

    raise TimeoutError(f"Request {request_id} did not finish within {args.timeout} seconds")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except requests.RequestException as exc:
        print(f"HTTP request failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
