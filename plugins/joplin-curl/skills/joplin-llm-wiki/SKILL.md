---
name: joplin-llm-wiki
description: "Maintain a Joplin-based LLM wiki: configure the notebook model, ingest raw sources into structured wiki notes, create and update wiki pages with appropriate tags, update index and log notes, lint for stale claims or missing links, and adapt Obsidian-oriented LLM wiki instructions to Joplin. Use when the user wants Codex to operate an LLM wiki in Joplin rather than Obsidian, or asks to process sources, create or update wiki notes, answer from the wiki, or keep the wiki structure consistent."
---

# Joplin LLM Wiki

Use Joplin as the wiki runtime.
Use the Joplin clipper API through the helper CLI.
Set `JOPLIN_API_PY` to the local path of `joplin_api.py` before using the command examples below.
Treat raw sources as immutable.
Treat wiki notes as LLM-maintained synthesis.

## Workflow

1. Check Joplin config:

```bash
python3 "$JOPLIN_API_PY" show-config
```

2. Verify connectivity before writes:

```bash
python3 "$JOPLIN_API_PY" ping
```

3. Inspect the existing notebook and note structure before creating new items:

```bash
python3 "$JOPLIN_API_PY" list-notebooks
python3 "$JOPLIN_API_PY" search --query "LLM Wiki" --fields id,parent_id,title
```

4. Read `LLM Wiki/Ops/Schema` before acting so task behavior follows the wiki's current operating rules. Use `search` to find the note ID, then fetch it with `get-note --note-id`; there is no `read-note` helper and `get-note` does not accept a positional ID. If the note is missing, continue with this skill's defaults and treat creating or repairing `Schema` as follow-up maintenance.

```bash
python3 "$JOPLIN_API_PY" search --query "Schema" --fields id,parent_id,title
python3 "$JOPLIN_API_PY" get-note --note-id NOTE_ID --fields id,title,body
```

5. Use the smallest API call that completes the task. Prefer helper subcommands. Use `request` when the helper surface is missing a needed notebook or tag operation.

## Notebook Model

Use this notebook layout unless the user already has a different stable convention:

- `LLM Wiki`
- `LLM Wiki/Raw Sources`
- `LLM Wiki/Wiki`
- `LLM Wiki/Ops`

Read [references/model.md](./references/model.md) for the role of each notebook and the core note set.

## Operating Rules

- Keep raw-source notes immutable except for metadata fixes.
- Put durable synthesis in `Wiki`.
- Put schema, prompts, and workflow rules in `Ops`.
- Read `LLM Wiki/Ops/Schema` before doing task work when that note exists.
- Keep one note per durable topic when practical.
- Keep `index` content-oriented.
- Keep `log` chronological and append-only.
- Preserve stable titles when updating existing notes.
- Prefer small updates over rewrites.
- Add tags when creating a wiki page or materially repurposing one and tags would improve retrieval, maintenance, or grouping.
- Reuse existing tags before creating new ones.
- Prefer a small set of high-signal tags over broad tag spam.
- Use tags for note type, topic, entity, source type, or workflow status when those dimensions help future search or maintenance.
- When adapting Obsidian-oriented instructions, replace vault/plugin assumptions with Joplin notebooks, note links, tags, clipper import, and search.

## Tagging

- Treat tags as selective metadata, not a required taxonomy for every note.
- Tag new `Wiki` pages when the page clearly belongs to a retrievable category such as a topic, entity, project, source family, or maintenance state.
- Tag `Raw Sources` when source type or intake status matters for later processing.
- Skip tags when the title, notebook location, and links already make the note easy to find.
- Search for an existing tag before creating a new one:

```bash
python3 "$JOPLIN_API_PY" search --type tag --query "TAG_NAME" --fields id,title
```

- If no suitable tag exists, create it with the generic API:

```bash
python3 "$JOPLIN_API_PY" request \
  --method POST \
  --path /tags \
  --data '{"title":"TAG_NAME"}'
```

- Attach a tag to a note with the generic API:

```bash
python3 "$JOPLIN_API_PY" request \
  --method POST \
  --path /tags/TAG_ID/notes \
  --data '{"id":"NOTE_ID"}'
```

## Common Tasks

### Ingest a source

1. Find or create the source note under `Raw Sources`.
2. Read the source note with `get-note --note-id NOTE_ID --fields id,title,body`.
3. Extract claims, entities, concepts, contradictions, and follow-up questions.
4. Update relevant notes in `Wiki`. Add or update tags on created or materially changed pages when useful.
5. Update `index`.
6. Append a dated `log` entry.

### Answer from the wiki

1. Read `index` first with `get-note --note-id NOTE_ID --fields id,title,body`.
2. Search relevant wiki notes.
3. Read only the notes needed with `get-note --note-id NOTE_ID --fields id,title,body`.
4. Answer with citations or Joplin note links when available.
5. Save durable analyses back into `Wiki` if the result should persist.

### Lint the wiki

Check for:

- stale claims
- contradictions
- orphan notes
- missing concept pages
- weak cross-links
- missing next-source suggestions

## Caveman Schema Pattern

When writing the operational schema note, use compressed, fact-dense sentences. Preserve constraints and structure. See [references/schema-caveman.md](./references/schema-caveman.md).

## Companion Skill

For first-time scaffold creation, use the companion skill `$joplin-llm-wiki-create`.
The requested label `joplin-llm-wiki:create` maps to that skill because Codex skill names use hyphens, not colons.
