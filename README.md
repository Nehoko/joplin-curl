# joplin-curl

Codex plugin for local Joplin notes, tags, and Joplin-backed LLM wiki workflows.

## What it does

- stores Joplin Web Clipper connection once in local JSON config
- exposes small `curl`-backed helper CLI for note and notebook tasks
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

## Configure Joplin

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

- `joplin-notes` - search, read, create, update, and organize Joplin notes through helper CLI
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

## Repo layout

- `.codex-plugin/plugin.json` - source plugin manifest
- `.agents/plugins/marketplace.json` - local Codex marketplace entry
- `plugins/joplin-curl/` - installable local plugin bundle for Codex
- `scripts/joplin_api.py` - helper CLI
- `skills/` - source skill docs
- `data/joplin-config.json` - local saved clipper config, ignored by git

## Notes

- plugin needs running local Joplin desktop app with Web Clipper enabled
- helper appends token as query parameter because Joplin Data API accepts auth that way
- `request` is fallback for API paths not covered by dedicated helper commands
