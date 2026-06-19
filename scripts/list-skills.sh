#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

find "$REPO_ROOT" -maxdepth 1 -type d ! -name '.*' ! -name 'template' -print0 \
  | while IFS= read -r -d '' dir; do
      if [[ -f "$dir/SKILL.md" ]]; then
        name="$(basename "$dir")"
        echo "$name"
      fi
    done \
  | sort
