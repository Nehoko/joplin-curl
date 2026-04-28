# joplin-curl

Codex plugin for local Joplin notes, notebook search, tag search, generic Joplin API calls, one-shot Joplin Terminal commands, and Joplin-backed LLM wiki workflows.

## What it does

- stores Joplin Web Clipper connection once in local JSON config when using the Data API
- exposes small helper CLI for curl-backed Data API tasks and one-shot Joplin Terminal commands
- bundles Codex skills for direct Joplin work and `LLM Wiki` maintenance
- supports local Codex marketplace install flow like `caveman`

## Install

### Codex local marketplace

```bash
git clone https://github.com/Nehoko/joplin-curl.git
cd joplin-curl
```

Open Codex in cloned repo, then:

1. open `/plugins`
2. search `Joplin Curl`
3. install local plugin from marketplace

Repo ships local marketplace metadata in `.agents/plugins/marketplace.json` and plugin bundle in `plugins/joplin-curl/`.

## Configure Joplin Data API

### 1. Enable Web Clipper in Joplin desktop

Official docs:

- [Joplin Web Clipper](https://joplinapp.org/help/apps/clipper/)
- [Joplin Data API](https://joplinapp.org/help/api/references/rest_api/)

In Joplin desktop:

1. open `Configuration`
2. open `Web Clipper`
3. enable clipper service
4. copy auth token

### 2. Point helper at bundled CLI

From repo root:

```bash
export JOPLIN_API_PY="$(pwd)/scripts/joplin_api.py"
```

If you want plugin-bundle path instead:

```bash
export JOPLIN_API_PY="$(pwd)/plugins/joplin-curl/scripts/joplin_api.py"
```

### 3. Save connection settings once

```bash
python3 "$JOPLIN_API_PY" set-config \
  --base-url http://127.0.0.1 \
  --port 41184 \
  --token YOUR_TOKEN
```

### 4. Verify

```bash
python3 "$JOPLIN_API_PY" show-config
python3 "$JOPLIN_API_PY" ping
```

## Included skills

- `joplin-notes` - search, read, create, update, and move Joplin notes, list or search notebooks, search tags, fall back to generic API requests, or run one-shot Joplin Terminal commands
- `joplin-llm-wiki` - maintain `LLM Wiki` notebooks with schema-first workflow
- `joplin-llm-wiki-create` - scaffold fresh Joplin wiki notebook tree and starter notes

## Common commands

```bash
python3 "$JOPLIN_API_PY" list-notebooks
python3 "$JOPLIN_API_PY" search --query "weekly review"
python3 "$JOPLIN_API_PY" get-note --note-id NOTE_ID
python3 "$JOPLIN_API_PY" create-note --title "Daily log" --body "..."
python3 "$JOPLIN_API_PY" update-note --note-id NOTE_ID --title "Updated"
python3 "$JOPLIN_API_PY" request --method GET --path /tags --query fields=id,title
```

## Joplin Terminal mode

Joplin Terminal can run commands directly from a shell, so Codex can execute a command and let the process exit without keeping Joplin Desktop open or Web Clipper enabled. Install it using the official [Joplin Terminal Application](https://joplinapp.org/help/apps/terminal/) instructions, then check it:

```bash
python3 "$JOPLIN_API_PY" check-terminal
```

Run one-shot Terminal commands by passing arguments after `terminal --`:

```bash
python3 "$JOPLIN_API_PY" terminal -- mkbook "My notebook"
python3 "$JOPLIN_API_PY" terminal -- use "My notebook"
python3 "$JOPLIN_API_PY" terminal -- mknote "My note"
python3 "$JOPLIN_API_PY" terminal -- ls -l
python3 "$JOPLIN_API_PY" terminal -- cat "My note"
python3 "$JOPLIN_API_PY" terminal -- set NOTE_ID title "New title"
python3 "$JOPLIN_API_PY" terminal -- mv NOTE_ID "Archive"
python3 "$JOPLIN_API_PY" terminal -- rmnote -f NOTE_ID
```

Use Data API mode when Joplin Desktop and Web Clipper are already running and JSON output is useful. Use Terminal mode when a one-shot local CLI command is enough.

## Repo layout

- `.codex-plugin/plugin.json` - source plugin manifest
- `.agents/plugins/marketplace.json` - local Codex marketplace entry
- `plugins/joplin-curl/` - installable local plugin bundle for Codex
- `scripts/joplin_api.py` - helper CLI
- `skills/` - source skill docs
- `data/joplin-config.json` - local saved clipper config, ignored by git

## Notes

- Data API mode needs running local Joplin desktop app with Web Clipper enabled
- Terminal mode needs the `joplin` terminal executable installed and available on `PATH`, or pass `--joplin-bin /path/to/joplin`
- helper appends token as query parameter because Joplin Data API accepts auth that way
- `request` is fallback for API paths not covered by dedicated helper commands
