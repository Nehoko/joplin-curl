# joplin-curl

Codex plugin for working with a local Joplin desktop client through the Joplin Data API.

## What it includes

- plugin manifest in `.codex-plugin/plugin.json`
- bundled skill in `skills/joplin-notes/`
- curl-backed helper CLI in `scripts/joplin_api.py`

## Setup

Save the Joplin clipper connection once:

```bash
python3 scripts/joplin_api.py set-config \
  --base-url http://127.0.0.1 \
  --port 41184 \
  --token YOUR_TOKEN
```

Check the stored config:

```bash
python3 scripts/joplin_api.py show-config
```

Verify connectivity:

```bash
python3 scripts/joplin_api.py ping
```

## Common commands

```bash
python3 scripts/joplin_api.py list-notebooks
python3 scripts/joplin_api.py search --query "weekly review"
python3 scripts/joplin_api.py get-note --note-id NOTE_ID
python3 scripts/joplin_api.py create-note --title "Daily log" --body "..."
python3 scripts/joplin_api.py update-note --note-id NOTE_ID --title "Updated"
```

## Notes

- local config is stored in `data/joplin-config.json`
- `data/` is ignored so tokens do not get committed
- the bundled skill is already included in this repository
