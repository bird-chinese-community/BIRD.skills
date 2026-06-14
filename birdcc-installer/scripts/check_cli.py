# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Check whether the birdcc CLI is installed without modifying the system."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys


def check_executable(name: str, version_flag: str = "--version") -> dict[str, object]:
    """Check whether an executable is on PATH and capture its version."""
    path = shutil.which(name)
    if not path:
        return {"installed": False, "version": None, "path": None}
    try:
        result = subprocess.run(
            [path, version_flag],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        output = result.stdout.strip() or result.stderr.strip()
        version = output.splitlines()[0] if output else None
    except (OSError, subprocess.TimeoutExpired):
        version = None
    return {"installed": True, "version": version, "path": path}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check whether the birdcc CLI is installed."
    )
    args = parser.parse_args(argv)

    result = {"birdcc": check_executable("birdcc")}

    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
