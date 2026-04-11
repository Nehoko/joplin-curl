---
name: joplin-llm-wiki-create
description: Create a fresh Joplin-based LLM wiki scaffold with the notebook tree, starter notes, index, log, source template, and compressed schema used for Joplin LLM wiki workflows. Use when the user wants to set up an LLM wiki in Joplin for the first time, recreate the scaffold in a new notebook tree, or asks for the `joplin-llm-wiki:create` workflow.
---

# Joplin LLM Wiki Create

Create the notebook scaffold first.
Do not duplicate existing structure unless the user asks.
Use the stored Joplin clipper config.
Set `JOPLIN_API_PY` to the local path of `joplin_api.py` before using the command examples below.

## Workflow

1. Verify Joplin config and connectivity:

```bash
python3 "$JOPLIN_API_PY" show-config
python3 "$JOPLIN_API_PY" ping
```

2. Check whether the wiki already exists:

```bash
python3 "$JOPLIN_API_PY" list-notebooks
python3 "$JOPLIN_API_PY" search --query "LLM Wiki" --fields id,parent_id,title
```

3. If no stable scaffold exists, create:

- root notebook `LLM Wiki`
- child notebooks `Raw Sources`, `Wiki`, `Ops`
- `Start Here`
- `Schema`
- `index`
- `log`
- `Source Intake Template`

4. If the root exists but children or notes are missing, add only the missing pieces.

5. Use real Joplin note links inside `index` after note creation.

## Folder Operations

Use `request` for notebook creation and movement because the helper has no dedicated folder-create command.

Examples:

```bash
python3 "$JOPLIN_API_PY" request --method POST --path /folders --data '{"title":"LLM Wiki"}'
python3 "$JOPLIN_API_PY" request --method PUT --path /folders/FOLDER_ID --data '{"title":"Raw Sources","parent_id":"ROOT_ID"}'
```

Use `create-note` and `update-note` for notes.

## Starter Bodies

Use the reference files as the default note bodies:

- [references/start-here.md](./references/start-here.md)
- [references/schema-caveman.md](./references/schema-caveman.md)
- [references/index-template.md](./references/index-template.md)
- [references/log-template.md](./references/log-template.md)
- [references/source-intake-template.md](./references/source-intake-template.md)

## Rules

- Prefer incremental creation over full reset.
- Preserve existing notebook IDs and note IDs.
- Do not rewrite user-authored notes unless the user asks.
- Normalize Obsidian-oriented instructions into Joplin-oriented wording.
- After creation, verify notebooks and at least one seed note via search.

## Naming Note

The requested sub-skill label `joplin-llm-wiki:create` is implemented as `$joplin-llm-wiki-create` because Codex skill names must use hyphens.
