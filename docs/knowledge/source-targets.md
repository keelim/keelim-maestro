# GBrain Source Targets

This file defines the first curated import pool for the workspace brain.

## Import Pool

| Source | Include | Reason |
| --- | --- | --- |
| Root workspace | `AGENTS.md`, `README.md`, `docs/**/*.md` | Root operating rules, codemaps, idea backlog, and research summaries |
| `Keelim-Knowledge-Vault` | Markdown notes and project index pages | Personal and technical knowledge base |
| `rich/docs/words` | Maintained wiki notes, raw-source operating docs, investing concepts, journal notes | Durable finance and operator knowledge |
| `youtube/docs` | Workflow, concept, decision, source-summary, and ops docs | Creator workflow memory |
| `youtube/packages` | Package markdown files | Shorts production package history and scripts |
| `keelim-plugin/skills` | `SKILL.md` and referenced markdown files | Local reusable skill knowledge |
| Active child repo entrypoints | `AGENTS.md`, `README.md`, and nested `AGENTS.md` where relevant | Child-specific operating rules without importing source code wholesale |

## Explicit Exclusions

- `.git/`, `.codegraph/`, `.omx/`, `.pytest_cache/`, `.ruff_cache/`
- `node_modules/`, `.next/`, `dist/`, `build/`, `coverage/`, render outputs,
  thumbnails, and other generated artifacts
- `.env`, `.env.*`, secret folders, credentials, API keys, tokens, database URLs
- Archived `toto/`
- Absent or no-remote `quant/`
- Broad child repository source trees unless a future import pass explicitly
  promotes them
- Sensitive `.raw/` sidecars unless reviewed and approved for the brain

## Source Identity

Use stable source ids when configuring GBrain sources:

- `root`
- `vault`
- `rich-words`
- `youtube-docs`
- `youtube-packages`
- `keelim-plugin-skills`
- `child-entrypoints`

When GBrain returns citations with `source_id`, preserve that source id in
answers and reports.

## Import Order

1. `root`
2. `child-entrypoints`
3. `vault`
4. `keelim-plugin-skills`
5. `rich-words`
6. `youtube-docs`
7. `youtube-packages`

This order keeps operating rules discoverable before deeper domain notes.
