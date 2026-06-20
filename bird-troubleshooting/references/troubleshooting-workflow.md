# BIRD Troubleshooting Workflow

## 1. Collect baseline

```bash
uv run scripts/collect_diagnostics.py --root .
```

Output includes:

- `birdcc` path and version
- `bird` path and version
- Detected `bird*.conf` files under `--root`

## 2. Gather the symptom

Ask the user for:

- Exact error message or log snippet
- BIRD version
- Relevant config snippet (redact secrets)
- What they expected vs what happened

## 3. Route by symptom type

| Symptom | Primary skill | Action |
| ------- | ------------- | ------ |
| Syntax / lint error | `bird-agent` | Run `birdcc lint` and fix config |
| Config passes but behavior wrong | `bird-agent` → `bird-source-explorer` | Check docs, then source |
| Daemon crash / assertion | `bird-source-explorer` | Map trace to source |
| Missing tooling | `birdcc-installer` | Install `birdcc` or `bird` |
| CI/CD failure | `birdcc-cicd` | Review workflow |

## 4. Synthesize answer

Present:

1. Most likely cause with evidence.
2. Alternative hypotheses.
3. One concrete next step per hypothesis.
