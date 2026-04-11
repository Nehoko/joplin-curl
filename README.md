# joplin-curl

Codex plugin for working with a local Joplin desktop client through the Joplin Data API.

## What it includes

- plugin manifest in `.codex-plugin/plugin.json`
- bundled skills in `skills/`
- curl-backed helper CLI in `scripts/joplin_api.py`
- local config storage in `data/joplin-config.json`

## Included skills

- `joplin-notes`: connect to the local Joplin clipper API and perform direct note, notebook, tag, and generic API tasks.
- `joplin-llm-wiki`: maintain a Joplin-backed LLM wiki with schema-first behavior, selective tagging, source ingest, and lint workflows.
- `joplin-llm-wiki-create`: scaffold the notebook tree and starter notes for a fresh Joplin LLM wiki.

## Setup

Set the helper path for skill command examples:

```bash
export JOPLIN_API_PY=/absolute/path/to/joplin_api.py
```

Inside this repository, that path is:

```bash
export JOPLIN_API_PY="$(pwd)/scripts/joplin_api.py"
```

Save the Joplin clipper connection once:

```bash
python3 "$JOPLIN_API_PY" set-config \
  --base-url http://127.0.0.1 \
  --port 41184 \
  --token YOUR_TOKEN
```

Check the stored config:

```bash
python3 "$JOPLIN_API_PY" show-config
```

Verify connectivity:

```bash
python3 "$JOPLIN_API_PY" ping
```

## Common commands

```bash
python3 "$JOPLIN_API_PY" list-notebooks
python3 "$JOPLIN_API_PY" search --query "weekly review"
python3 "$JOPLIN_API_PY" get-note --note-id NOTE_ID
python3 "$JOPLIN_API_PY" create-note --title "Daily log" --body "..."
python3 "$JOPLIN_API_PY" update-note --note-id NOTE_ID --title "Updated"
```

## Notes

- all bundled skills assume `JOPLIN_API_PY` points at the helper script
- local config is stored in `data/joplin-config.json` relative to `joplin_api.py`
- `data/` is ignored so tokens do not get committed
- the plugin repository is the source of truth for all Joplin-related skills
