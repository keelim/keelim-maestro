# all

Last reviewed: 2026-04-13

## Signals

- Multi-module Android/KMP workspace with six app modules and a wide shared core.
- Strong platform surface already exists in `core:*`, `feature:*`, widgets, and
  custom Gradle build logic.
- Release and quality risk scale quickly when several apps move in parallel.

## Open ideas

### 2026-04-12 - Shared module adoption map

Status: proposed

Why now: Shared Android/KMP modules already span several apps, so the highest-leverage refactors are easier to find when duplication and reuse are visible in one matrix.

First slice: Generate an app-to-module dependency map from the Gradle graph, then rank the duplicate flows or utilities that should be consolidated first.

### 2026-04-12 - Cross-app feature flag registry

Status: proposed

Why now: The workspace already has enough shared architecture that rollout
controls can pay off across several apps at once instead of being rebuilt per
app.

First slice: Define a shared flag schema and local cache, then expose a small
developer-facing screen in one app before promoting it into a shared module.

### 2026-04-12 - Release readiness radar

Status: proposed

Why now: A family of apps plus shared modules creates hidden release drift
around versioning, QA coverage, changelog completeness, and regression risk.

First slice: Generate a single report that gathers per-app version, pending
release notes, test/build status, and any known rollout blockers.
