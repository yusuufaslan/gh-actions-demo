#!/usr/bin/env python3
import os
import sys
from huggingface_hub import HfApi

space_id = os.environ.get("SPACE_ID", "")
if not space_id:
    if len(sys.argv) > 1:
        space_id = sys.argv[1]
    else:
        print("ERROR: SPACE_ID not set")
        sys.exit(1)

api = HfApi()

try:
    api.create_repo(
        repo_id=space_id,
        repo_type="space",
        space_sdk="gradio",
        exist_ok=True,
    )
    print("Space mevcut veya olusturuldu.")
except Exception as e:
    if "already exists" in str(e):
        print("Space zaten mevcut.")
    else:
        raise
