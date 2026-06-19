# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Detect which editor the user is likely working with from workspace signals."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path

EDITOR_SIGNALS: list[tuple[str, str]] = [
    # Workspace-level signals
    (".vscode/settings.json", "vscode"),
    (".vscode/extensions.json", "vscode"),
    (".vscode/launch.json", "vscode"),
    (".cursorrules", "cursor"),
    (".cursor/settings.json", "cursor"),
    (".idea", "jetbrains"),
    (".idea/misc.xml", "jetbrains"),
    (".idea/vcs.xml", "jetbrains"),
    # Neovim/Vim config files (often in project root or home)
    ("init.lua", "neovim"),
    ("init.vim", "neovim"),
    (".vimrc", "vim"),
    ("_vimrc", "vim"),
    (".gvimrc", "vim"),
    (".nvimrc", "neovim"),
    # Windsurf / Trae / Kiro (OpenVSX-based forks)
    (".windsurf/settings.json", "windsurf"),
    (".trae/settings.json", "trae"),
]

HOME_EDITOR_FILES: dict[str, str] = {
    ".config/nvim/init.lua": "neovim",
    ".config/nvim/init.vim": "neovim",
    ".vimrc": "vim",
    ".vsvimrc": "vim",
}

# Map the first token of ``git config core.editor`` to a canonical editor id.
GIT_EDITOR_ALIASES: dict[str, str] = {
    "vi": "vim",
    "vim": "vim",
    "nvim": "neovim",
    "neovim": "neovim",
    "code": "vscode",
    "code-insiders": "vscode-insiders",
    "codium": "vscodium",
    "cursor": "cursor",
    "windsurf": "windsurf",
    "trae": "trae",
    "kiro": "kiro",
    "idea": "jetbrains",
    "idea.sh": "jetbrains",
    "idea64.exe": "jetbrains",
    "goland": "jetbrains",
    "pycharm": "jetbrains",
    "webstorm": "jetbrains",
    "clion": "jetbrains",
}


def _run_text(cmd: list[str], cwd: Path | None = None, timeout: float = 8) -> str | None:
    """Run a command and return decoded stdout, treating decode errors as a missing result."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
        return result.stdout.strip() or None
    except (OSError, subprocess.TimeoutExpired, UnicodeDecodeError):
        return None


def detect_workspace_signals(root: Path) -> list[dict[str, str]]:
    """Return workspace editor signals as normalized objects."""
    signals: list[dict[str, str]] = []
    for rel_path, editor in EDITOR_SIGNALS:
        candidate = root / rel_path
        if candidate.exists():
            signals.append({"source": "workspace", "path": rel_path, "editor": editor})
    return signals


def detect_home_signals() -> list[dict[str, str]]:
    """Return home-directory editor signals as normalized objects."""
    home = Path.home()
    signals: list[dict[str, str]] = []
    for rel_path, editor in HOME_EDITOR_FILES.items():
        candidate = home / rel_path
        if candidate.exists():
            signals.append(
                {"source": "home", "path": str(candidate), "editor": editor}
            )
    return signals


def detect_git_editor(root: Path) -> list[dict[str, str]]:
    """Return a signal for ``git config core.editor`` if it resolves to a known editor."""
    raw = _run_text(["git", "config", "--get", "core.editor"], cwd=root)
    if not raw:
        return []

    tokens = shlex.split(raw)
    if not tokens:
        return []

    alias = Path(tokens[0]).name.lower()
    editor = GIT_EDITOR_ALIASES.get(alias)
    if not editor:
        return []

    return [{"source": "git", "path": raw, "editor": editor}]


def compute_confidence(editors: list[str]) -> str:
    """Return high/medium/low/none based on signal diversity."""
    if not editors:
        return "none"
    unique = set(editors)
    if len(unique) == 1:
        return "high"
    if len(unique) <= 2:
        return "medium"
    return "low"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Detect the user's editor from workspace and home-directory signals."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Project root to scan (default: current directory).",
    )
    parser.add_argument(
        "--include-home",
        action="store_true",
        help="Also scan the user's home directory for editor config files.",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if not root.is_dir():
        json.dump(
            {"error": f"root is not a directory: {root}"},
            sys.stderr,
            indent=2,
            ensure_ascii=False,
        )
        sys.stderr.write("\n")
        return 2

    workspace_signals = detect_workspace_signals(root)
    home_signals = detect_home_signals() if args.include_home else []
    git_signals = detect_git_editor(root)

    all_signals = workspace_signals + home_signals + git_signals
    all_signals.sort(key=lambda s: (s["source"], s["path"], s["editor"]))
    editors = [s["editor"] for s in all_signals]
    detected = sorted(set(editors))

    result = {
        "root": str(root),
        "detected_editors": detected,
        "signals": all_signals,
        "confidence": compute_confidence(editors),
    }

    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
