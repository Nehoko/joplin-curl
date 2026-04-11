---
name: joplin-notes
description: Use this skill when Codex needs to read, search, create, update, or organize notes in a local Joplin desktop client through the Joplin Data API. Trigger when the user asks to work with Joplin notes, notebooks, tags, todos, clipper API, or to persist and reuse a local Joplin host, port, and token across future tasks.
---

# Joplin Notes

## Overview

Use the bundled helper CLI to store Joplin clipper connection settings once, then reuse them for note and notebook tasks.
Keep requests minimal. Prefer the smallest command or API call that completes the task.

## Workflow

1. Check whether config already exists:

```bash
python3 /Users/iliamikhailov/work/plugins/joplin-curl/scripts/joplin_api.py show-config
```

2. If config is missing or the user wants to change it, ask for `http address`, `port`, and `token`, then store them:

```bash
python3 /Users/iliamikhailov/work/plugins/joplin-curl/scripts/joplin_api.py set-config \
  --base-url http://127.0.0.1 \
  --port 41184 \
  --token YOUR_TOKEN
```

3. Verify connectivity before destructive work:

```bash
python3 /Users/iliamikhailov/work/plugins/joplin-curl/scripts/joplin_api.py ping
```

4. Run the narrowest helper command for the task. Use `request` only when a dedicated command is missing.

## Common Commands

List notebooks:

```bash
python3 /Users/iliamikhailov/work/plugins/joplin-curl/scripts/joplin_api.py list-notebooks
```

Search notes:

```bash
python3 /Users/iliamikhailov/work/plugins/joplin-curl/scripts/joplin_api.py search \
  --query "weekly review" \
  --fields id,parent_id,title
```

Get a note:

```bash
python3 /Users/iliamikhailov/work/plugins/joplin-curl/scripts/joplin_api.py get-note \
  --note-id NOTE_ID
```

Create a note:

```bash
python3 /Users/iliamikhailov/work/plugins/joplin-curl/scripts/joplin_api.py create-note \
  --title "Daily log" \
  --body "- item 1" \
  --parent-id NOTEBOOK_ID
```

Update a note:

```bash
python3 /Users/iliamikhailov/work/plugins/joplin-curl/scripts/joplin_api.py update-note \
  --note-id NOTE_ID \
  --title "Updated title"
```

Generic API call:

```bash
python3 /Users/iliamikhailov/work/plugins/joplin-curl/scripts/joplin_api.py request \
  --method GET \
  --path /tags \
  --query fields=id,title
```

## Rules

- Use the stored config by default. Do not ask for host, port, or token again unless config is missing or the user wants to edit it.
- Prefer helper subcommands over raw `request`.
- Use `search` or `list-notebooks` first when the user names a note or notebook by title instead of ID.
- Confirm `ping` succeeds before create, update, or delete operations.
- Read [`references/commands.md`](./references/commands.md) for the command surface and config path details.
