# all-web-ui

Last reviewed: 2026-04-13

## Signals

- Shared React UI package consumed by multiple web repos.
- Already ships theme tokens and reusable primitives such as `button`, `panel`,
  `badge`, and loading/empty states.
- Shared UI releases create coupling, so confidence and discoverability matter.

## Open ideas

### 2026-04-12 - Token playground and theme diff lab

Status: proposed

Why now: Shared theme tokens are more valuable when consumers can preview what a
 token change will do before publishing it into downstream apps.

First slice: Build a tiny docs/demo page that renders each primitive under the
 existing themes and highlights token deltas side by side.

### 2026-04-12 - Visual regression and accessibility gate pack

Status: proposed

Why now: A shared component package becomes much safer to evolve when visual and
 accessibility regressions are caught before they break `keelim-vercel` or
 `rich/web`.

First slice: Add snapshot coverage for the exported primitives plus a minimal
 accessibility check in CI for the demo surface.

### 2026-04-12 - Downstream usage matrix

Status: proposed

Why now: The package already powers multiple web apps, so changes are safer
when the consumer graph and upgrade surface are visible in one place.

First slice: Generate a matrix of exported primitives vs downstream import
sites, then attach a short upgrade checklist for each consumer repo.
