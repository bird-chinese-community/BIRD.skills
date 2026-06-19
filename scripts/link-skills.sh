#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIRS=("$HOME/.claude/skills" "$HOME/.codex/skills")

for target in "${TARGET_DIRS[@]}"; do
  if [[ ! -d "$target" ]]; then
    mkdir -p "$target"
    echo "created directory: $target"
  fi
done

mapfile -t skills < <("$REPO_ROOT/scripts/list-skills.sh")

if [[ ${#skills[@]} -eq 0 ]]; then
  echo "no skills found in $REPO_ROOT" >&2
  exit 1
fi

for skill in "${skills[@]}"; do
  src="$REPO_ROOT/$skill"
  for target in "${TARGET_DIRS[@]}"; do
    dest="$target/$skill"
    if [[ -e "$dest" ]]; then
      if [[ -L "$dest" ]]; then
        current_target="$(readlink "$dest")"
        if [[ "$current_target" == "$src" ]]; then
          echo "already linked: $dest -> $src"
          continue
        fi
      fi
      echo "refusing to overwrite existing path: $dest" >&2
      continue
    fi
    ln -s "$src" "$dest"
    echo "linked: $dest -> $src"
  done
done
