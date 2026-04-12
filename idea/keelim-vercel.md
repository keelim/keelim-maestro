# keelim-vercel

Last reviewed: 2026-04-13

## Signals

- Large Next.js finance product with many calculator and dashboard routes.
- Mixes Supabase-backed content, market data, newsletter flows, and persistent
  client storage.
- The current surface is wide, which makes cross-tool continuity more valuable
  than adding isolated single-purpose pages forever.

## Open ideas

### 2026-04-12 - Tool usage heatmap and dead-surface cleanup

Status: proposed

Why now: The app already tracks `tool_clicks` and exposes a wide route inventory, so usage data can drive pruning and promotion instead of manual guesswork.

First slice: Produce a weekly report that ranks tools by real usage, flags long-unused surfaces, and suggests consolidation candidates.

### 2026-04-12 - Shared financial profile and scenario workspace

Status: proposed

Why now: Many tools likely ask for overlapping assumptions such as income,
 family state, savings pace, debt, tax context, and risk preference.

First slice: Introduce a reusable user profile plus named scenarios so several
 calculators can prefill from the same assumptions instead of starting cold.

### 2026-04-12 - Next-best-action feed across finance tools

Status: proposed

Why now: The product has enough calculators, market widgets, and saved surfaces
 that users would benefit from guidance on what to do next instead of choosing
 from a long catalog every time.

First slice: Build a small recommendation panel that uses recent tool history,
 bookmarks, and a few profile signals to suggest the next relevant workflow.
