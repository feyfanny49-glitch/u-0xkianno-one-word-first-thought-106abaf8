#!/usr/bin/env python3
"""One Word, First Thought: write exactly one judged word to /output/entry.txt.

The artifact is written as UTF-8 bytes with no trailing newline and published
with mode 0644, which the grader requires. Standard library only, so it runs
in the Python 3.13 sandbox.
"""

from __future__ import annotations

import hashlib
import os
import stat
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
    """Publish the artifact and verify its exact bytes and mode."""
    data = validated_bytes()
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / ARTIFACT_NAME

    # Ask for 0644 at creation so the file is never briefly world-inaccessible,
    # and refuse a symlink planted at the destination. chmod still forces the
    # exact mode when the umask is restrictive (or a file already existed).
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW
    fd = os.open(destination, flags, MODE)
    with os.fdopen(fd, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(destination, MODE)

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
