"""Download KiCad API proto files and compile to Python."""

import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO = "kicad%2Fcode%2Fkicad"
BRANCH = "10.0.0-rc2"
PROTO_PATH = "api/proto"
GITLAB_API = f"https://gitlab.com/api/v4/projects/{REPO}"

ROOT = Path(__file__).parent.parent
PROTO_SRC = ROOT / "proto_src"
PROTO_OUT = ROOT / "src" / "kicad_mcp" / "proto"


def list_proto_files():
    url = f"{GITLAB_API}/repository/tree?path={PROTO_PATH}&recursive=true&per_page=100&ref={BRANCH}"
    with urllib.request.urlopen(url) as resp:
        items = json.loads(resp.read())
    return [item["path"] for item in items if item["type"] == "blob" and item["path"].endswith(".proto")]


def download_file(path: str):
    encoded = urllib.request.quote(path, safe="")
    url = f"{GITLAB_API}/repository/files/{encoded}/raw?ref={BRANCH}"
    rel = path.removeprefix(f"{PROTO_PATH}/")
    dest = PROTO_SRC / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"  {rel}")
    urllib.request.urlretrieve(url, dest)


def compile_protos():
    proto_files = list(PROTO_SRC.rglob("*.proto"))
    if not proto_files:
        print("No proto files found!")
        sys.exit(1)

    # Ensure output dirs exist
    PROTO_OUT.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable, "-m", "grpc_tools.protoc",
        f"--proto_path={PROTO_SRC}",
        f"--python_out={PROTO_OUT}",
    ] + [str(f) for f in proto_files]

    print(f"Compiling {len(proto_files)} proto files...")
    subprocess.check_call(cmd)

    # Fix imports: protoc generates absolute imports like "from common.types import ..."
    # We need them relative: "from kicad_mcp.proto.common.types import ..."
    fix_imports(PROTO_OUT)

    # Create __init__.py files
    create_init_files(PROTO_OUT)

    print("Done!")


def fix_imports(proto_out: Path):
    """Fix protoc-generated imports to use package-relative paths."""
    for pb2 in proto_out.rglob("*_pb2.py"):
        text = pb2.read_text()
        original = text
        # Replace imports like:
        #   from common.types import base_types_pb2
        #   from board import board_types_pb2
        for prefix in ["common.", "common.types.", "common.commands.", "board.", "schematic."]:
            text = text.replace(
                f"from {prefix.rstrip('.')} import",
                f"from kicad_mcp.proto.{prefix.rstrip('.')} import"
            )
            text = text.replace(
                f"from {prefix}",
                f"from kicad_mcp.proto.{prefix}"
            )
        if text != original:
            pb2.write_text(text)
            print(f"  Fixed imports in {pb2.name}")


def create_init_files(proto_out: Path):
    for dirpath in proto_out.rglob("*"):
        if dirpath.is_dir():
            init = dirpath / "__init__.py"
            if not init.exists():
                init.write_text("")
    init = proto_out / "__init__.py"
    if not init.exists():
        init.write_text("")


def main():
    print(f"Downloading proto files from KiCad {BRANCH}...")
    proto_files = list_proto_files()
    print(f"Found {len(proto_files)} proto files:")
    for path in proto_files:
        download_file(path)

    print()
    compile_protos()


if __name__ == "__main__":
    main()
