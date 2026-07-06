"""Deploy helper script for pushing a Gradio app to a HuggingFace Space."""

import os
import sys
from huggingface_hub import HfApi


SPACE_ID = os.environ.get("HF_SPACE_ID", "yusuf-aslan/text-tools")


def ensure_space() -> None:
    """Create the Space if it does not already exist."""
    api = HfApi()
    try:
        api.create_repo(
            repo_id=SPACE_ID,
            repo_type="space",
            space_sdk="gradio",
            exist_ok=True,
        )
        print(f"[OK]  Space '{SPACE_ID}' mevcut veya olusturuldu.")
    except Exception as exc:
        if "already exists" in str(exc):
            print(f"[OK]  Space '{SPACE_ID}' zaten mevcut.")
        else:
            raise


def upload_files() -> None:
    """Upload the application files to the Space."""
    api = HfApi()
    files = [
        ("src/app.py", "app.py"),
        ("requirements.txt", "requirements.txt"),
        ("Dockerfile", "Dockerfile"),
    ]

    for local_path, remote_path in files:
        if not os.path.exists(local_path):
            print(f"[WARN] '{local_path}' bulunamad, atlan.")
            continue
        print(f"[UP]  {local_path} -> {remote_path}")
        api.upload_file(
            path_or_fileobj=local_path,
            path_in_repo=remote_path,
            repo_id=SPACE_ID,
            repo_type="space",
        )

    print("[OK]  Dosyalar Space'a yuklendi.")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "all"

    if command == "ensure-space":
        ensure_space()
    elif command == "upload":
        upload_files()
    elif command == "all":
        ensure_space()
        upload_files()
    else:
        print(f"[ERR] Unknown command: {command}")
        sys.exit(1)
