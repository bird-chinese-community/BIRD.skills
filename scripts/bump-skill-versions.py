# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Bump the version of every BIRD skill manifest and keep them consistent.

Usage:
    uv run scripts/bump-skill-versions.py 1.2.3
    uv run scripts/bump-skill-versions.py 1.2.3 --dry-run
    uv run scripts/bump-skill-versions.py 1.2.3 --no-sync-marketplaces
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import subprocess
import sys
from pathlib import Path


VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
FRONTMATTER_VERSION_RE = re.compile(
    r"^(\s+version:\s*)['\"]?[^'\"\n]*['\"]?$", re.MULTILINE
)


def discover_skills(root: Path) -> list[str]:
    skills: list[str] = []
    for entry in sorted(root.iterdir()):
        if (
            entry.is_dir()
            and not entry.name.startswith(".")
            and entry.name != "template"
            and (entry / "SKILL.md").is_file()
            and (entry / "metadata.json").is_file()
        ):
            skills.append(entry.name)
    return skills


def load_json(path: Path) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"  ⚠️  skipping invalid JSON {path}: {exc}")
        return None


def save_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_json_version(path: Path, new_version: str, dry_run: bool) -> bool:
    if not path.is_file():
        return False
    data = load_json(path)
    if data is None:
        return False

    changed = False

    def bump(node: object, path_parts: list[str]) -> object:
        nonlocal changed
        if isinstance(node, dict):
            new_node: dict[str, object] = {}
            for k, v in node.items():
                if (
                    k == "version"
                    and isinstance(v, str)
                    and VERSION_RE.match(v)
                    and v != new_version
                ):
                    new_node[k] = new_version
                    changed = True
                    print(f"  ✏️  {path}: {'/'.join(path_parts + [k])} -> {new_version}")
                else:
                    new_node[k] = bump(v, path_parts + [k])
            return new_node
        if isinstance(node, list):
            return [bump(item, path_parts + [f"[{i}]"]) for i, item in enumerate(node)]
        return node

    new_data = bump(data, [])
    if changed and not dry_run:
        save_json(path, new_data)
    return changed


def update_skill_frontmatter(skill_dir: Path, new_version: str, dry_run: bool) -> bool:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return False
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    if end == -1:
        return False
    frontmatter = text[3:end]
    rest = text[end:]
    new_frontmatter, count = FRONTMATTER_VERSION_RE.subn(
        f'\\1"{new_version}"', frontmatter
    )
    if count == 0:
        return False
    print(
        f"  ✏️  {skill_md}: metadata.version -> {new_version} ({count} occurrence{'s' if count > 1 else ''})"
    )
    if not dry_run:
        skill_md.write_text("---" + new_frontmatter + rest, encoding="utf-8")
    return True


def sync_root_plugin_json(root: Path, skills: list[str], new_version: str, dry_run: bool) -> bool:
    path = root / "plugin.json"
    data = load_json(path)
    if data is None or not isinstance(data, dict):
        return False

    changed = False

    if isinstance(data.get("version"), str) and data["version"] != new_version:
        data["version"] = new_version
        changed = True
        print(f"  ✏️  {path}: version -> {new_version}")

    expected_skills = sorted(f"./{s}" for s in skills)
    if data.get("skills") != expected_skills:
        data["skills"] = expected_skills
        changed = True
        print(f"  ✏️  {path}: skills -> {expected_skills}")

    expected_agents = sorted(
        f"./{s}/agents" for s in skills if (root / s / "agents").is_dir()
    )
    if data.get("agents") != expected_agents:
        data["agents"] = expected_agents
        changed = True
        print(f"  ✏️  {path}: agents -> {expected_agents}")

    if changed and not dry_run:
        save_json(path, data)
    return changed


def skill_abstract(skill_dir: Path) -> str | None:
    meta = load_json(skill_dir / "metadata.json")
    if isinstance(meta, dict):
        abstract = meta.get("abstract")
        if isinstance(abstract, str):
            return abstract
    return None


def default_category(marketplace_path: Path, fallback: str = "development") -> str:
    # .agents/plugins uses "Coding"; GitHub/Cursor/Claude marketplaces use "development"/"integration".
    if ".agents" in marketplace_path.parts:
        return "Coding"
    return fallback


def sync_marketplace_plugins(
    root: Path, skills: list[str], new_version: str, dry_run: bool
) -> bool:
    changed_any = False
    for path in sorted(root.rglob("marketplace.json")):
        rel_parts = path.relative_to(root).parts
        if any(
            part in (".git", "node_modules", ".worktrees", ".venv", "__pycache__")
            for part in rel_parts
        ):
            continue

        data = load_json(path)
        if not isinstance(data, dict):
            continue

        plugins = data.get("plugins")
        if not isinstance(plugins, list) or not plugins:
            continue

        template = plugins[0]
        if not isinstance(template, dict):
            continue

        existing_by_name: dict[str, dict[str, object]] = {}
        for entry in plugins:
            if isinstance(entry, dict) and isinstance(entry.get("name"), str):
                existing_by_name[entry["name"]] = entry

        changed = False
        for skill in skills:
            abstract = skill_abstract(root / skill)
            if abstract is None:
                abstract = skill.replace("-", " ")

            if skill in existing_by_name:
                entry = existing_by_name[skill]
                if isinstance(entry.get("version"), str) and entry["version"] != new_version:
                    entry["version"] = new_version
                    changed = True
                    print(f"  ✏️  {path}: plugins/{skill}/version -> {new_version}")
                continue

            new_entry: dict[str, object] = copy.deepcopy(template)
            new_entry["name"] = skill
            new_entry["description"] = abstract
            new_entry["version"] = new_version

            # Source format varies by marketplace
            if isinstance(new_entry.get("source"), dict):
                new_entry["source"] = {"source": "local", "path": f"./{skill}"}
            else:
                new_entry["source"] = f"./{skill}"

            # Category: keep existing if present, otherwise default
            if "category" in new_entry:
                new_entry["category"] = default_category(path)

            plugins.append(new_entry)
            existing_by_name[skill] = new_entry
            changed = True
            print(f"  ✏️  {path}: added plugin entry for {skill}")

        if changed:
            # Keep a deterministic order
            data["plugins"] = sorted(plugins, key=lambda e: str(e.get("name", "")))
            changed_any = True
            if not dry_run:
                save_json(path, data)

    return changed_any


def repo_root() -> Path:
    try:
        toplevel = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        return Path(toplevel)
    except Exception:
        return Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bump BIRD skill version across all manifests"
    )
    parser.add_argument("version", help="New semver version, e.g. 1.2.3")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print changes without writing files",
    )
    parser.add_argument(
        "--sync-marketplaces",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="Ensure all marketplace.json files list every discovered skill",
    )
    args = parser.parse_args()

    if not VERSION_RE.match(args.version):
        print(f"Invalid semver version: {args.version}")
        return 1

    root = repo_root()
    print(f"Working in {root}")
    print(f"New version: {args.version}")
    if args.dry_run:
        print("DRY RUN — no files will be modified\n")

    skills = discover_skills(root)
    print(f"Discovered skills: {', '.join(skills)}\n")

    changed_any = False

    # Skill-level manifests
    for skill in skills:
        print(f"Processing skill: {skill}")
        skill_dir = root / skill
        changed_any |= update_json_version(
            skill_dir / "metadata.json", args.version, args.dry_run
        )
        changed_any |= update_skill_frontmatter(skill_dir, args.version, args.dry_run)
        changed_any |= update_json_version(
            skill_dir / "plugin.json", args.version, args.dry_run
        )
        print()

    # Root plugin manifest
    changed_any |= sync_root_plugin_json(root, skills, args.version, args.dry_run)

    # Other top-level manifests
    for manifest_name in ("plugin.json", "marketplace.json"):
        for path in sorted(root.rglob(manifest_name)):
            rel_parts = path.relative_to(root).parts
            if any(
                part in (".git", "node_modules", ".worktrees", ".venv", "__pycache__")
                for part in rel_parts
            ):
                continue
            changed_any |= update_json_version(path, args.version, args.dry_run)

    # package.json (top-level only)
    changed_any |= update_json_version(root / "package.json", args.version, args.dry_run)

    # Marketplace plugin lists
    if args.sync_marketplaces:
        changed_any |= sync_marketplace_plugins(root, skills, args.version, args.dry_run)

    print()
    if args.dry_run:
        print("Dry run complete; no files were modified.")
    elif changed_any:
        print("All manifests updated. Review with `git diff` and commit.")
    else:
        print("No version changes were needed.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
