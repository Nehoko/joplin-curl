# Notebook Model

## Root

`LLM Wiki` is the container notebook.

## Child notebooks

- `Raw Sources`: imported markdown, clipped articles, papers, transcripts, images, and source notes. Treat as immutable source-of-truth notes.
- `Wiki`: topic notes, entity notes, comparisons, summaries, and durable answers.
- `Ops`: schema, prompts, templates, and maintenance rules.

## Core notes

Seed these notes for a new wiki:

- `Start Here`: human-readable overview of how this Joplin wiki works.
- `Schema`: compressed operating rules for the LLM maintainer.
- `index`: entry point with links to the main notes.
- `log`: chronological record of setup, ingest, query, and lint actions.
- `Source Intake Template`: template for a raw-source note before ingest.

## Joplin substitutions

Replace Obsidian-specific assumptions with:

- notebooks instead of vault directories
- Joplin Web Clipper or markdown import instead of Obsidian Web Clipper
- note links and search instead of graph view
- tags as optional metadata, not a required system
