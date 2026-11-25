#!/usr/bin/env python3
"""One Word, First Thought: write exactly one judged word to /output/entry.txt.

The artifact is written atomically, with mode 0644, as UTF-8 bytes with no
trailing newline. Standard library only, so it runs in the Python 3.13 sandbox.
"""

from __future__ import annotations

import hashlib
import os
import stat
import tempfile
from pathlib import Path

WORD = "mooncalf"
OUTPUT_DIR = Path("/output")
ARTIFACT_NAME = "entry.txt"
MODE = 0o644


def validated_bytes() -> bytes:
    """Return the exact artifact bytes, or fail loudly before touching /output."""
    if not isinstance(WORD, str) or not (1 <= len(WORD) <= 24) or not WORD.strip():
        raise ValueError("artifact must be 1-24 non-whitespace characters")
    if any(ch.isspace() or ord(ch) < 32 for ch in WORD):
        raise ValueError("artifact must be exactly one word, with no whitespace or controls")
    if WORD != WORD.strip() or "\ufeff" in WORD:
        raise ValueError("artifact must carry no BOM or padding")
    data = WORD.encode("utf-8")
    if data.decode("utf-8") != WORD or b"\n" in data or b"\r" in data:
        raise ValueError("artifact must round-trip as UTF-8 without a newline")
    return data


def write_artifact(output_dir: Path = OUTPUT_DIR) -> Path:
    """Atomically publish the artifact and verify its bytes and mode."""
    data = validated_bytes()
    output_dir.mkdir(parents=True, exist_ok=True)

    # A crashed earlier run may have left a temp file; /output must hold only
    # the required artifact. Only touch files this program names with its prefix.
    for stale in output_dir.glob(".entry-*"):
        if stale.is_file():
            stale.unlink()

    destination = output_dir / ARTIFACT_NAME
    fd, temp_name = tempfile.mkstemp(prefix=".entry-", dir=str(output_dir))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        # mkstemp creates 0600, which the grader refuses: fix it BEFORE replace.
        os.chmod(temp_name, MODE)
        os.replace(temp_name, destination)
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise

    # Durably record the rename, then check the published file itself.
    dir_fd = os.open(str(output_dir), os.O_RDONLY)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)

    mode = stat.S_IMODE(destination.stat().st_mode)
    if mode != MODE:
        raise OSError(f"artifact mode {mode:04o} is not {MODE:04o}")
    if destination.read_bytes() != data:
        raise OSError("published artifact bytes differ from the validated word")
    return destination


def main() -> None:
    path = write_artifact()
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {path}: {len(WORD)} chars, {len(data)} bytes, sha256 {digest}, mode 0644")


if __name__ == "__main__":
    main()
