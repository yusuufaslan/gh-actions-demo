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

local_path = os.environ.get("LOCAL_PATH", "")
remote_path = os.environ.get("REMOTE_PATH", "")

if not local_path or not remote_path:
    print("ERROR: LOCAL_PATH and REMOTE_PATH must be set")
    sys.exit(1)

if not os.path.isfile(local_path):
    print(f"UYARI: {local_path} bulunamadi, atlan.")
    sys.exit(0)

api = HfApi()
api.upload_file(
    path_or_fileobj=local_path,
    path_in_repo=remote_path,
    repo_id=space_id,
    repo_type="space",
)
print(f"Yuklendi: {local_path} -> {remote_path}")
