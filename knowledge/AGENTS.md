# XiaoAn Legal Mechanism Wiki Guidelines

## Purpose

This `knowledge/` folder is an LLM-maintained legal mechanism wiki for XiaoAn, a domestic-violence first-response assistant. The current scope is the middle layer only: read immutable legal sources and maintain a source-grounded legal mechanism tree.

Core model:

```text
knowledge/source/           # raw legal sources, user-owned, LLM read-only
        |
        v
knowledge/wiki/             # legal mechanism tree, LLM-maintained
        |-- nodes/           # legal atoms as graph nodes
        |-- edges.md         # legal mechanisms as graph edges/relations
        |-- legal-mechanism-tree.md
        |
        v
scenario capsules           # future product layer, not maintained now
```

## Layers

- `knowledge/source/`: immutable raw legal sources. The user owns this layer. Never edit, rewrite, rename, summarize in place, or normalize source files unless the user explicitly asks.
- `knowledge/wiki/nodes/`: LLM-owned legal atom nodes. Each page should represent one legal concept, right, duty, remedy, actor, procedure, condition, evidence type, or consequence.
- `knowledge/wiki/edges.md`: LLM-owned legal mechanism edge catalog. Each edge states how two legal nodes relate, with source references.
- `knowledge/wiki/legal-mechanism-tree.md`: root page for browsing the current graph.
- `knowledge/index.md`: content catalog for the legal mechanism tree. Update whenever a node or edge is created, renamed, or materially changed.
- `knowledge/log.md`: chronological append-only activity log. Add an entry for every legal-source ingest, durable legal synthesis, or lint pass.
- `knowledge/knowledge_strategy.md`: product and knowledge strategy context. Keep wiki changes aligned with it.

Out of current scope:

- Do not create or edit `knowledge/wiki/sources/` source-summary pages.
- Do not create or edit `knowledge/wiki/scenario-capsules/` unless the user explicitly starts scenario-capsule work.
- Do not turn legal mechanisms into a separate page layer. Mechanisms are edges/relations between legal atom nodes.

## Wiki Page Conventions

- Use Markdown files with YAML frontmatter.
- Prefer Chinese for domain knowledge pages unless the source or task requires English.
- Use stable, lowercase, hyphenated filenames for wiki pages.
- Use Obsidian-style links such as `[[domestic-violence-definition]]` for internal cross-references.
- Every synthesized claim that may influence user guidance must cite raw source references in a `source_refs` field or a `## 来源依据` section.
- Distinguish source text, legal interpretation, and product-facing guidance. Do not collapse them into an uncited recommendation.
- Mark unresolved conflicts, gaps, or uncertainty explicitly instead of smoothing them over.

Recommended frontmatter:

```yaml
---
type: legal-node | legal-edge-catalog | legal-mechanism-tree | legal-synthesis
title: ""
source_refs:
  - "knowledge/source/example.md#第十五条"
updated: YYYY-MM-DD
status: draft | reviewed | needs-review
---
```

Legal node frontmatter should also include:

```yaml
node_kind: definition | actor | duty | right | remedy | procedure | evidence | consequence | support
```

## Ingest Workflow

1. Read new raw legal sources in `knowledge/source/` without modifying them.
2. Extract or update legal atom nodes under `knowledge/wiki/nodes/`.
3. Add or update legal mechanism edges in `knowledge/wiki/edges.md`.
4. Update `knowledge/wiki/legal-mechanism-tree.md` so the graph remains browsable in Obsidian.
5. Update `knowledge/index.md`.
6. Append one entry to `knowledge/log.md`.

## Legal Mechanism Tree Rules

Legal mechanisms are not a separate layer of pages. A mechanism is an edge: a sourced relationship between two legal atom nodes.

- Use source-backed nodes and source-backed edges, not free-form advice.
- Keep atomic legal claims in `nodes/`.
- Keep relationship metadata in `edges.md`.
- Express graph links using Obsidian links in node pages so the graph view remains useful.
- Link the tree root to raw source filenames so Obsidian can visualize source-to-mechanism coverage without editing raw sources.
- Prefer relationship labels such as `defines_scope_for`, `triggers`, `requires`, `enables`, `provides_evidence_for`, `assists_execution_of`, `limits`, `creates_consequence_for`, and `parallel_support_channel_for`.

Scenario capsules are a later product layer and should remain untouched unless the user explicitly asks to work on them.

## Query Workflow

1. Read `knowledge/index.md` first.
2. Open relevant node pages in `knowledge/wiki/nodes/`.
3. Open `knowledge/wiki/edges.md` for sourced relationships between nodes.
4. Answer with source-grounded synthesis and cite node/source references.
5. If the answer reveals a durable legal node or edge, update the wiki and log it. Do not create scenario capsules by default.

## Lint Workflow

Periodically check for:

- nodes with no source references;
- edges whose source or target node does not exist;
- important raw sources not yet represented in the graph;
- duplicate nodes for the same legal concept;
- edge claims that overstate what the source says;
- national/local rule conflicts or local refinements that need explicit edge labels;
- Obsidian links that do not resolve.

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
