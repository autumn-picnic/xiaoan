# Project Guidelines

## Purpose

This repository is an LLM-maintained legal mechanism wiki for XiaoAn, a domestic-violence first-response assistant. The current scope is the middle layer only: read immutable legal sources and maintain a source-grounded legal mechanism tree.

## Layers

- `knowledge/source/`: immutable raw legal sources. The user owns this layer. Never edit, rewrite, rename, summarize in place, or normalize source files unless the user explicitly asks.
- `knowledge/wiki/legal-atoms/`: LLM-owned atomic legal units extracted from sources.
- `knowledge/wiki/legal-mechanisms/`: LLM-owned legal mechanism tree. This is the primary maintained layer.
- `knowledge/index.md`: content catalog for the legal mechanism tree. Update whenever a legal atom or mechanism page is created, renamed, or materially changed.
- `knowledge/log.md`: chronological append-only activity log. Add an entry for every legal-source ingest, durable legal synthesis, or lint pass.
- `README.md`, `knowledge/knowledge_strategy.md`, and `tech/code/architecture.md`: product and architecture context. Keep wiki changes aligned with these docs.

Out of current scope:

- Do not create or edit `knowledge/wiki/sources/` source-summary pages.
- Do not create or edit `knowledge/wiki/scenario-capsules/` unless the user explicitly starts scenario-capsule work.

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
    type: legal-mechanism-tree | legal-atom | legal-mechanism | legal-synthesis
title: ""
source_refs:
  - "knowledge/source/example.md#第十五条"
updated: YYYY-MM-DD
status: draft | reviewed | needs-review
---
```

## Ingest Workflow

1. Read new raw legal sources in `knowledge/source/` without modifying them.
2. Extract or update legal atoms under `knowledge/wiki/legal-atoms/`.
3. Update the legal mechanism tree under `knowledge/wiki/legal-mechanisms/`.
4. Keep `knowledge/wiki/legal-mechanisms/legal-mechanism-tree.md` as the tree root.
5. Update `knowledge/index.md`.
6. Append one entry to `knowledge/log.md`.

## Legal Mechanism Tree Rules

Legal mechanism pages are not user scripts. They should explain how legal concepts, duties, remedies, procedures, evidence, and institutional responsibilities connect.

- Use source-backed nodes, not free-form advice.
- Keep atomic legal claims in `legal-atoms/`.
- Keep cross-source synthesis and mechanism explanations in `legal-mechanisms/`.
- Link mechanisms to their supporting atoms using Obsidian links.
- Link the tree root to raw source filenames so Obsidian can visualize source-to-mechanism coverage without editing raw sources.

Scenario capsules are a later product layer and should remain untouched unless the user explicitly asks to work on them.

## Safety and Legal Boundaries

- High-risk signals override knowledge retrieval in product use. If the user is in immediate danger, prioritize crisis SOP behavior over legal completeness.
- Never invent institutions, hotline numbers, shelter addresses, case law, or local procedures.
- Do not promise outcomes such as "police will definitely handle it" or "the court will approve it."
- For individual legal strategy, frame content as rights education and suggest professional legal aid when needed.
- Preserve privacy: do not store raw user PII in wiki pages or examples.

## Maintenance

- When answering a legal question produces durable synthesis, file it back into the legal mechanism tree and index it.
- Periodically lint the legal mechanism tree for orphan pages, stale claims, missing citations, duplicate concepts, and source coverage gaps.
- Prefer small, well-cited pages over long uncited essays.
