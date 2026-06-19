# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Validate skill directory structure and SKILL.md frontmatter."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED_TOP_LEVEL = {"name", "description", "license", "metadata"}
REQUIRED_METADATA = {"version"}
REQUIRED_METADATA_JSON = {
    "name",
    "version",
    "organization",
    "date",
    "abstract",
    "references",
    "requires",
}
SCRIPT_RE = re.compile(r"\]\((scripts/[a-zA-Z0-9_\-./]+)\)")


def _indent_level(line: str) -> int:
    return len(line) - len(line.lstrip())


def _unfold_scalar(lines: list[str], start: int, base_indent: int) -> tuple[str, int]:
    parts: list[str] = []
    i = start
    while i < len(lines):
        line = lines[i]
        if line.strip() == "":
            i += 1
            continue
        if _indent_level(line) < base_indent:
            break
        parts.append(line.strip())
        i += 1
    return " ".join(parts), i


def _parse_frontmatter(text: str) -> dict[str, object]:
    data: dict[str, object] = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == "" or line.strip().startswith("#"):
            i += 1
            continue
        match = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)\s*$", line)
        if not match:
            i += 1
            continue
        key, value = match.group(1), match.group(2).strip()
        if value == ">":
            folded, i = _unfold_scalar(lines, i + 1, _indent_level(line) + 2)
            data[key] = folded
        elif value == "":
            # Possibly a nested mapping (e.g. metadata:)
            nested: dict[str, object] = {}
            base_indent = _indent_level(line) + 2
            i += 1
            while i < len(lines):
                inner = lines[i]
                if inner.strip() == "" or inner.strip().startswith("#"):
                    i += 1
                    continue
                if _indent_level(inner) < base_indent:
                    break
                inner_match = re.match(r"^\s+([A-Za-z0-9_\-]+):\s*(.*)\s*$", inner)
                if inner_match:
                    nested[inner_match.group(1)] = (
                        inner_match.group(2).strip().strip('"')
                    )
                i += 1
            data[key] = nested
        else:
            data[key] = value.strip('"')
            i += 1
    return data


def _extract_frontmatter(skill_md: Path) -> dict[str, object] | None:
    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return None
    end = content.find("\n---", 3)
    if end == -1:
        return None
    return _parse_frontmatter(content[3:end])


def _referenced_scripts(skill_md: Path) -> list[str]:
    content = skill_md.read_text(encoding="utf-8")
    return sorted(set(SCRIPT_RE.findall(content)))


def check_skill(skill_dir: Path) -> dict[str, object]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.is_file():
        errors.append("missing SKILL.md")
        return {"name": skill_dir.name, "ok": False, "errors": errors}

    frontmatter = _extract_frontmatter(skill_md)
    if frontmatter is None:
        errors.append("missing or malformed YAML frontmatter")
        return {"name": skill_dir.name, "ok": False, "errors": errors}

    missing_top = REQUIRED_TOP_LEVEL - set(frontmatter.keys())
    if missing_top:
        errors.append(f"missing top-level frontmatter keys: {sorted(missing_top)}")

    metadata = frontmatter.get("metadata")
    if isinstance(metadata, dict):
        missing_meta = REQUIRED_METADATA - set(metadata.keys())
        if missing_meta:
            errors.append(f"missing metadata keys: {sorted(missing_meta)}")
    else:
        errors.append("metadata must be a mapping")

    metadata_json = skill_dir / "metadata.json"
    if not metadata_json.is_file():
        errors.append("missing metadata.json")
    else:
        try:
            meta = json.loads(metadata_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid metadata.json: {exc}")
            meta = {}
        missing_meta_json = REQUIRED_METADATA_JSON - set(meta.keys())
        if missing_meta_json:
            errors.append(
                f"missing metadata.json keys: {sorted(missing_meta_json)}"
            )
        if not isinstance(meta.get("references"), list):
            errors.append("metadata.json 'references' must be a list")
        requires = meta.get("requires", {})
        if not isinstance(requires, dict) or not isinstance(
            requires.get("bins"), list
        ):
            errors.append("metadata.json 'requires.bins' must be a list")

    for ref in _referenced_scripts(skill_md):
        script_path = skill_dir / ref
        if not script_path.is_file():
            errors.append(f"missing referenced script: {ref}")

    return {
        "name": str(frontmatter.get("name", skill_dir.name)),
        "ok": len(errors) == 0,
        "errors": errors,
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    results: list[dict[str, object]] = []

    for entry in sorted(repo_root.iterdir()):
        if (
            entry.is_dir()
            and not entry.name.startswith(".")
            and entry.name != "template"
        ):
            if (entry / "SKILL.md").exists():
                results.append(check_skill(entry))

    ok = all(bool(r["ok"]) for r in results)
    report = {"ok": ok, "skills": results}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
