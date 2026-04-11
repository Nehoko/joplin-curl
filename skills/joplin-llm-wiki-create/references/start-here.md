# LLM Wiki in Joplin

This notebook adapts the `llm-wiki.md` pattern to Joplin.

## Model

- `Raw Sources` stores imported or clipped source material. Treat these notes as immutable.
- `Wiki` stores LLM-maintained synthesis notes: concepts, entities, comparisons, summaries, and answers worth keeping.
- `Ops` stores the schema, workflow rules, and maintenance notes that tell the LLM how to operate.

## Joplin-specific replacements

- Use Joplin notebooks instead of an Obsidian vault layout.
- Use Joplin Web Clipper or markdown import instead of Obsidian Web Clipper.
- Use note links, notebook structure, and tags instead of Obsidian graph view and Dataview.
- Keep `index` and `log` notes current so navigation stays simple without external RAG.

## Workflow

### Ingest

1. Add a new note to `Raw Sources`.
2. Ask the LLM to read it.
3. Create or update summary and concept notes in `Wiki`.
4. Update `index`.
5. Append a dated entry to `log`.

### Query

1. Search `index` first.
2. Read the most relevant `Wiki` notes.
3. Answer with citations or note links.
4. Save durable analyses back into `Wiki` when they are worth keeping.

### Lint

Periodically ask the LLM to check for stale claims, contradictions, orphan notes, weak cross-links, and missing topic pages.
