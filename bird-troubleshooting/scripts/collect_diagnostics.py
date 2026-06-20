# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Collect baseline BIRD tooling diagnostics."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> str | None:
    exe = shutil.which(cmd[0])
    if not exe:
        return None
    try:
        result = subprocess.run(
            [exe, *cmd[1:]],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        return (result.stdout.strip() or result.stderr.strip()) or None
    except Exception as exc:
        return f"error: {exc}"


def _is_within_root(path: Path, root: Path) -> bool:
    """Return True if path is the same as or inside root after resolving symlinks."""
    try:
        path.resolve().relative_to(root.resolve())
    except (ValueError, OSError):
        return False
    return True


def detect_configs(root: Path) -> list[str]:
    configs: list[str] = []
    seen: set[Path] = set()
    for path in root.rglob("*.conf"):
        if path in seen:
            continue
        seen.add(path)
        name = path.name.lower()
        if not (name.startswith("bird") and name.endswith(".conf")):
            continue
        # Guard against symlink escapes and unusual filesystem entries.
        if not path.is_file() or path.is_symlink():
            continue
        if not _is_within_root(path, root):
            continue
        try:
            configs.append(str(path.relative_to(root)))
        except ValueError:
            configs.append(str(path))
    return sorted(configs)


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect BIRD diagnostics")
    parser.add_argument("--root", default=".", help="Workspace root to scan")
    args = parser.parse_args()

    root = Path(args.root).resolve()

    data = {
        "birdcc_bin": shutil.which("birdcc"),
        "birdcc_version": run(["birdcc", "--version"]),
        "bird_bin": shutil.which("bird"),
        "bird_version": run(["bird", "--version"]),
        "config_files": detect_configs(root),
    }

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
