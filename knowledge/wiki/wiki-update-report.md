---
type: wiki-update-report
title: "Wiki Update Report（来源 POC 历史快照）"
generated_at: 2026-06-28T01:46:59+00:00
imported_at: 2026-07-12
status: historical
---

# Wiki Update Report

> ⚠️ 此文件从 `xiaoan-poc-capsule-chatflow` 导入，仅记录来源 POC 当时的检查结果；它不是当前仓库 `knowledge/source/` 的最新扫描结果，也不代表下列断链状态仍然有效。

- generated_at: `2026-06-28T01:46:59+00:00`
- manifest: `knowledge/wiki/source-manifest.json`
- previous_manifest_updated_at: `2026-06-28T01:46:10+00:00`
- current_source_count: 32
- changed_source_count: 0
- manifest_written: false

## Source changes

| status | count |
|---|---:|
| added | 0 |
| modified | 0 |
| deleted | 0 |

### Added
- none

### Modified
- none

### Deleted
- none

## Affected wiki pages

- none

## Broken source_refs

| page | source_ref | error |
|---|---|---|
| `knowledge/wiki/nodes/temporary-shelter.md` | `knowledge/source/中国反家庭暴力法律法规与司法解释.md#告诫制度意见` | anchor not found in source: 告诫制度意见 |

## Changed source files with no wiki references

- none

## Manual update workflow

1. Review added/modified/deleted source files above.
2. For each affected wiki page, update `knowledge/wiki/nodes/*.md`, `edges.md`, or syntheses as needed.
3. For added sources with no wiki references, decide whether to create a new node or attach the source to existing nodes.
4. For deleted sources, remove or replace stale `source_refs` before running chatflow.
5. Re-run this script until broken refs are gone.
6. After the wiki layer is updated and reviewed, re-run with `--write-manifest` to accept the current source snapshot.

Suggested command:

```bash
.venv/bin/python tech/chatflow/poc/wiki_update.py
.venv/bin/python tech/chatflow/poc/wiki_update.py --write-manifest
```
