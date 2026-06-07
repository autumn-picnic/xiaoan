# Project Guidelines

## Purpose

This repository is an LLM-maintained knowledge wiki for XiaoAn, a domestic-violence first-response assistant. The goal is not generic RAG; it is a persistent, source-grounded wiki that turns raw legal and practice materials into safer, lower-burden support knowledge.

## Layers

- `knowledge/source/`: immutable raw sources. Treat these as the source of truth. Do not rewrite source content except to fix source metadata or obvious transcription errors.
- `knowledge/wiki/`: LLM-owned synthesized wiki pages. Create and update these pages when ingesting sources or answering durable knowledge questions.
- `knowledge/index.md`: content catalog. Update whenever a wiki page is created, renamed, or materially changed.
- `knowledge/log.md`: chronological append-only activity log. Add an entry for every ingest, durable query page, or lint pass.
- `README.md`, `knowledge/knowledge_strategy.md`, and `tech/code/architecture.md`: product and architecture context. Keep wiki changes aligned with these docs.

## Wiki Page Conventions

- Use Markdown files with YAML frontmatter.
- Prefer Chinese for domain knowledge pages unless the source or task requires English.
- Use stable, lowercase, hyphenated filenames for wiki pages.
- Use Obsidian-style links (`[[page-name]]`) for internal cross-references.
- Every synthesized claim that may influence user guidance must cite raw source references in a `source_refs` field or a `## 来源依据` section.
- Distinguish source text, legal interpretation, and product-facing guidance. Do not collapse them into an uncited recommendation.
- Mark unresolved conflicts, gaps, or uncertainty explicitly instead of smoothing them over.

Recommended frontmatter:

```yaml
---
type: source-summary | legal-atom | legal-mechanism | scenario-capsule | synthesis
title: ""
source_refs:
  - "knowledge/source/example.md#第十五条"
updated: YYYY-MM-DD
status: draft | reviewed | needs-review
---
```

## Ingest Workflow

1. Read the new raw source in `knowledge/source/`.
2. Create or update a source summary page under `knowledge/wiki/sources/`.
3. Extract legal atoms under `knowledge/wiki/legal-atoms/` when the source contains actionable legal units.
4. Update mechanism pages under `knowledge/wiki/legal-mechanisms/` for cross-source synthesis.
5. Update or create scenario capsules under `knowledge/wiki/scenario-capsules/` only when the source supports a concrete user pain point.
6. Update `knowledge/index.md`.
7. Append one entry to `knowledge/log.md`.

## Scenario Capsule Rules

Scenario capsules are the product-facing layer. Each capsule should include:

- `Trigger`: concrete user phrasing or situation.
- `Recognize`: a short, non-judgmental reframe that reduces self-blame or confusion.
- `Act`: 1-3 low-burden next steps, with safety caveats.
- `Ground`: source-grounded legal or practical basis and its limits.
- `Related topics`: links to adjacent capsules or legal mechanisms.
- `Safety override`: red flags that should bypass the capsule and route to crisis handling.

Do not make a capsule sound like guaranteed legal advice. Use it to support the main agent's response, not to force a rigid script.

## Safety and Legal Boundaries

- High-risk signals override knowledge retrieval. If the user is in immediate danger, prioritize crisis SOP behavior over legal completeness.
- Never invent institutions, hotline numbers, shelter addresses, case law, or local procedures.
- Do not promise outcomes such as "police will definitely handle it" or "the court will approve it."
- For individual legal strategy, frame content as rights education and suggest professional legal aid when needed.
- Preserve privacy: do not store raw user PII in wiki pages or examples.

## Maintenance

- When answering a question produces durable synthesis, file it back into `knowledge/wiki/` and index it.
- Periodically lint the wiki for orphan pages, stale claims, missing citations, duplicate concepts, and outdated scenario capsules.
- Prefer small, well-cited pages over long uncited essays.
