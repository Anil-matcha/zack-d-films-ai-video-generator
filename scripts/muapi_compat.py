#!/usr/bin/env python3
"""
Small compatibility bridge for the shared MuAPI client.
"""

from provider import APIClient, get_client

MuAPIClient = APIClient


if __name__ == "__main__":
    client = MuAPIClient()
    result = client.generate_image(
        "Stylized 3D boy swallowing pink bubble gum, macro stomach cross section"
    )
    print("[MuAPI Client] Test OK:", result["status"])
