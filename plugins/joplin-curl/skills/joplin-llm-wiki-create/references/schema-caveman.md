Purpose: persistent wiki in Joplin.

Human curate sources.
LLM maintain wiki.

Raw Sources immutable.
Wiki notes synthetic.
Ops notes operational.

Notebook model:
- Raw Sources: clipped articles, imported markdown, papers, transcripts, images, data.
- Wiki: topic notes, entity notes, summaries, comparisons, question outputs worth keeping.
- Ops: schema, prompts, workflows, templates.

Ingest flow:
- read source note.
- extract claims.
- write source summary.
- update relevant wiki notes.
- flag contradiction.
- append log entry.
- update index entry.

Query flow:
- read index first.
- select candidate notes.
- synthesize answer.
- cite note titles or links.
- save durable result back into Wiki.

Lint flow:
- find stale claims.
- find orphan notes.
- find missing backlinks.
- find missing concept pages.
- find contradiction.
- suggest next sources.

Note rules:
- one note, one topic.
- summary first.
- claims explicit.
- uncertainty explicit.
- sources linked.
- related notes linked.
- open questions listed.

Maintenance rules:
- prefer small updates.
- preserve stable titles.
- do not edit raw-source notes except metadata fixes.
- keep index content-oriented.
- keep log chronological.
- tags optional. notebook structure primary.
