---
name: joplin-notes
description: Use this skill when Codex needs to read, search, create, update, or move notes in Joplin through the local Data API or one-shot Joplin Terminal commands. Trigger when the user asks to work with Joplin notes, list or search notebooks, search tags, make a generic Joplin API request for unsupported endpoints such as todos or tag changes, persist and reuse a local Joplin base URL, port, and token, or use Joplin without keeping Desktop Web Clipper open.
---

# Joplin Notes

## Overview

Use the bundled helper CLI to store Joplin clipper connection settings once, then reuse them for note, notebook, search, and generic Joplin API tasks.
When the user does not want to keep Joplin Desktop and Web Clipper open, use Joplin Terminal mode for one-shot CLI commands.
Set `JOPLIN_API_PY` to the local path of `joplin_api.py` before using the command examples below.
Keep requests minimal. Prefer the smallest command or API call that completes the task.

## Workflow

1. Check whether config already exists:

```bash
python3 "$JOPLIN_API_PY" show-config
```

2. If config is missing or the user wants to change it, ask for `http address`, `port`, and `token`, then store them:

```bash
python3 "$JOPLIN_API_PY" set-config \
  --base-url http://127.0.0.1 \
  --port 41184 \
  --token YOUR_TOKEN
```

3. Verify connectivity before destructive work:

```bash
python3 "$JOPLIN_API_PY" ping
```

4. Run the narrowest helper command for the task. Use `request` only when a dedicated API command is missing, such as for folder creation, tag attachment, or todo-specific fields.
5. Use Terminal mode instead of Data API mode when the task should run without a running Joplin Desktop Web Clipper service.

## Common Commands

List notebooks:

```bash
python3 "$JOPLIN_API_PY" list-notebooks
```

Search notes:

```bash
python3 "$JOPLIN_API_PY" search \
  --query "weekly review" \
  --fields id,parent_id,title
```

Search notebooks or tags:

```bash
python3 "$JOPLIN_API_PY" search \
  --query "project" \
  --type folder \
  --fields id,parent_id,title
```

Get a note:

```bash
python3 "$JOPLIN_API_PY" get-note \
  --note-id NOTE_ID
```

Create a note:

```bash
python3 "$JOPLIN_API_PY" create-note \
  --title "Daily log" \
  --body "- item 1" \
  --parent-id NOTEBOOK_ID
```

Update a note:

```bash
python3 "$JOPLIN_API_PY" update-note \
  --note-id NOTE_ID \
  --title "Updated title"
```

Generic API call:

```bash
python3 "$JOPLIN_API_PY" request \
  --method GET \
  --path /tags \
  --query fields=id,title
```

Check Joplin Terminal:

```bash
python3 "$JOPLIN_API_PY" check-terminal
```

Run a one-shot Joplin Terminal command:

```bash
python3 "$JOPLIN_API_PY" terminal -- mknote "Daily log"
```

Terminal CRUD examples:

```bash
python3 "$JOPLIN_API_PY" terminal -- cat NOTE_ID
python3 "$JOPLIN_API_PY" terminal -- set NOTE_ID title "Updated title"
python3 "$JOPLIN_API_PY" terminal -- mv NOTE_ID "Archive"
python3 "$JOPLIN_API_PY" terminal -- rmnote -f NOTE_ID
```

## Rules

- Use the stored config by default. Do not ask for host, port, or token again unless config is missing or the user wants to edit it.
- Prefer helper subcommands over raw `request`.
- Use `search` or `list-notebooks` first when the user names a note or notebook by title instead of ID.
- Confirm `ping` succeeds before create, update, or delete operations.
- For Terminal mode, confirm `check-terminal` succeeds before create, update, move, or delete operations.
- Pass `--joplin-bin /path/to/joplin` before the subcommand when `joplin` is not on `PATH`.
- Read [`references/commands.md`](./references/commands.md) for the command surface and config path details.
