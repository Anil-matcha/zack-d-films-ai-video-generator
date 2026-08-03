#!/usr/bin/env python3
"""
Backward compatibility bridge for Higgsfield API client.
"""

from provider import APIClient, get_client

# Alias for backward compatibility
HiggsfieldClient = APIClient

if __name__ == "__main__":
    client = HiggsfieldClient()
    res = client.generate_image("Stylized 3D boy swallowing pink bubble gum, macro stomach cross section")
    print("[API Client] Test OK:", res["status"])
