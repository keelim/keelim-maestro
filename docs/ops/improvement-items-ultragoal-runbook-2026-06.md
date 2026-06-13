# Improvement Items Ultragoal Runbook — 2026-06

This runbook keeps the 800-item improvement backlog executable across long
`/goal` continuations.

## Source Of Truth

- Viewer: `docs/research/improvement-items-viewer-2026-06.html`
- Stable inventory: `docs/research/improvements-2026-06/improvements.json`
- Task slices: `docs/research/improvements-2026-06/raw/*.json`
- Progress ledger:
  - `docs/ops/improvement-items-progress-2026-06.json`
  - `docs/ops/improvement-items-progress-2026-06.md`

## Resume Checklist

1. Run `omx ultragoal status --json`.
2. Run `get_goal` and confirm the active objective is the aggregate Ultragoal
   objective from `.omx/ultragoal/goals.json`.
3. Run `python3 scripts/improvements/init_progress_ledger.py --check`.
4. Read the `assigned`, `in_progress`, `blocked`, and `needs_consumer_check`
   rows in the progress ledger before spawning or editing anything.
5. If no workers are active, pick the next `todo` task by wave order.

## Worker Contract

Each worker owns exactly one `project + dimension` raw JSON file. Workers must:

- Work only inside the owning child repository.
- Read root `AGENTS.md` and the child repo `AGENTS.md` before edits.
- Preserve existing dirty work and never revert unrelated changes.
- Avoid editing the root progress ledger or `.omx/ultragoal`; the leader owns
  those files.
- Report handled backlog IDs, changed files, verification commands/results,
  and blockers.

## Leader Contract

The leader must:

- Keep root coordination state in `docs/ops`.
- Update task/item status only from worker evidence.
- Run `bun run report:baseline` before and after the aggregate run.
- Run `bun run report:shared-ui` when `all-web-ui` public contracts or
  `keelim-vercel`/`rich` shared UI consumers change.
- Checkpoint Ultragoal only with fresh `get_goal` snapshots.
- Run the final Ultragoal cleanup/review gate before `update_goal`.

## Current Assignments

| task | worker | scope |
|---|---|---|
| `T07-all-web-ui-a11y` | Jason | `all-web-ui` a11y backlog |
| `T32-youtube-reliability` | Maxwell | `youtube` reliability backlog |

## Verified Task Units

| task | worker | evidence |
|---|---|---|
| `T01-android-support-ci-release` | Lovelace | 19 selected ledger items verified with CI/release workflow checks, tests, coverage, build, bundle freshness, and `git diff --check`. |
| `T02-android-support-dx-docs` | Chandrasekhar | 13 selected ledger items verified with split upload/sign README docs, credential and release-note precedence docs, declared runtime outputs, README/action/runtime contract parser coverage, clean contract drift check, 11 passing suites / 174 tests / 100% coverage, typecheck, ESLint, ci-release check, build, and `git diff --check`. |
| `T03-android-support-error-handling` | Lovelace | 18 selected ledger items verified with contextual error handling, retry/timeout guards, response validation, expanded tests, rebuilt bundle, and CI/release checks. |
| `T04-android-support-security` | Darwin | 17 selected ledger items verified with Android release action security hardening, path/archive/credential guard coverage, 11 passing suites / 169 tests / 100% coverage, contract and ci-release checks, rebuilt `lib/index.js`, and `git diff --check`. |
| `T05-android-support-testing` | Lovelace | 18 selected ledger items verified with contract drift check, typecheck, test lint, unit tests, coverage, ncc build, CI/release workflow check, and `git diff --check`; leader rerun reported 9 suites / 144 tests / 100% coverage. |
| `T06-android-support-type-safety` | Wegener | 15 selected ledger items verified with stricter TypeScript compiler options, typed release status/upload options, explicit Google API response data guards, ESLint, 11 passing suites / 172 tests / 100% coverage, contract and ci-release checks, rebuilt `lib/index.js`, and `git diff --check`. |
| `T08-all-web-ui-api-design` | Carson | 17 selected ledger items verified with API/theme/telemetry contract hardening, public prop and variant exports, scoped theme contract metadata, 35 passing Bun tests / 748 expects, typecheck, build, design lint, package smoke, npm pack dry-run, root shared-ui report, and `git diff --check`; root shared-ui full gate still carries only `rich/web` primitive drift to `T43`. |
| `T09-all-web-ui-component-quality` | Halley | 14 selected ledger items verified with polymorphic component refs, normalized component primitives, portal/animation-aware interaction coverage, 34 passing Bun tests / 493 expects, package smoke, npm pack dry-run, root shared-ui report, and `git diff --check`; root shared-ui full gate still carries only `rich/web` primitive drift to `T43`. |
| `T10-all-web-ui-docs` | Planck | 17 selected ledger items verified with README/DESIGN style-contract docs, manifest style/theme metadata, Stitch metadata hash refresh, design lint, typecheck, 35 passing Bun tests / 597 expects, build, package smoke, npm pack dry-run, root shared-ui report, and `git diff --check`; root shared-ui full gate still carries only `rich/web` primitive drift to `T43`. |
| `T11-all-web-ui-packaging` | Turing | 17 selected ledger items verified with package publish gates, dist contract verifier, consumer smoke, npm pack dry-run, release-version guard, typecheck, 31 passing Bun tests / 463 expects, build, and `git diff --check`; root shared-ui full gate still carries only `rich/web` primitive drift to `T43`. |
| `T12-all-web-ui-testing` | Helmholtz | 19 selected ledger items verified with DOM interaction coverage, Progress aria value propagation, RadioGroup keyboard movement coverage, standalone `bun.lock` refresh, typecheck, 31 passing Bun tests / 459 expects, build, and `git diff --check`; root shared-ui report still surfaces consumer-side follow-up drift for `T24`/`T43`. |
| `T13-keelim-plugin-docs` | Russell | 14 selected ledger items verified with README/catalog workflow docs, deterministic catalog generator checks, 8/8 skill metadata validation, full repo check, pre-commit all-files, and `git diff --check`. |
| `T14-keelim-plugin-dx-tooling` | Euler | 15 selected ledger items verified with CI/pre-commit/full-check tooling, deterministic skill/catalog validation, uv dev tooling, `bash scripts/check.sh`, pre-commit all-files, and `git diff --check`. |
| `T15-keelim-plugin-script-quality` | Laplace | 21 selected ledger items verified with Python compile checks, bundled script tests, skill verification, catalog check, SkillOpt validation, and `git diff --check`. |
| `T16-keelim-plugin-security` | Laplace | 17 selected ledger items verified with path/env guard changes, script/skill security regression tests, SkillOpt eval checks, skill/catalog checks, and leader rerun of `uv --cache-dir .skillopt/uv-cache run --python 3.12 python scripts/run-tests.py`. |
| `T17-keelim-plugin-skill-quality` | Lorentz | 14 selected ledger items verified with skill-quality regression checks in `verify_skills.py`, tightened skill docs/references, ticket desk fallback test, catalog regeneration, `bash scripts/check.sh`, pre-commit all-files, and `git diff --check`. |
| `T18-keelim-plugin-testing-evals` | Laplace | 19 selected ledger items verified with repo-local test/eval runner, SkillOpt validation, score fixtures, skill/catalog checks, durable eval file visibility, and `git diff --check`. |
| `T20-keelim-vercel-api-correctness` | Schrodinger | 20 selected ledger items verified with authenticated API contracts, data envelopes, validation/error guards, CSV/SSRF limits, route tests, typecheck, build, maintenance check, and `git diff --check`. |
| `T21-keelim-vercel-component-quality` | Linnaeus | 14 selected ledger items verified with native button/sibling-button interaction fixes, accessible names and label wiring for icon buttons, selects, sliders, and search inputs, AGENTS lesson update, typecheck, lint with 0 errors / 13 existing warnings, 51 passing tests, production build, `verify:maintenance`, root shared-ui report, and `git diff --check`; root shared-ui full gate still carries only `rich/web` primitive drift to `T43`. |
| `T22-keelim-vercel-dx-config` | Lagrange | 11 selected ledger items verified with CI/pre-push/PR quality gates, typed ESLint/test/strict TS scaffolding, Drizzle/Supabase config guards, centralized env schema access, shared UI client shim build fix, 51 passing Bun tests / 179 expects, production build, `verify:maintenance`, root shared-ui report, and `git diff --check`; `typecheck:strict` remains a baseline-finding gate. |
| `T23-keelim-vercel-security` | Schrodinger | 17 selected ledger items verified with production auth allowlist, route/server-action validation, SSRF/CSV/rate-limit guards, typecheck, 39-test Bun suite, production build, maintenance checks, scoped ESLint, and `git diff --check`. |
| `T24-keelim-vercel-testing` | Feynman | 15 selected ledger items verified with selected API route regression tests, route mapping verifier, full tests/coverage, typecheck, lint, build, `verify:maintenance`, and `git diff --check`; root shared-ui full gate now passes `keelim-vercel` adapters and carries only the `rich/web` primitive drift to `T43`. |
| `T34-youtube-testing` | Erdos | 21 selected ledger items verified with youtube pytest coverage gate, 135 passing tests, 90.30% coverage, `git diff --check`, root `uv.lock` refresh, `uv lock --check`, and Python dependency constraint verification. |
| `T35-keelim-knowledge-vault-automation` | Codex | 18 selected ledger items verified with vault-wide backlink JSON/file checks, resurface check/threshold behavior, schema/template contract checks, Obsidian properties/templates config checks, workspace cleanup checks, verifier compile, and `git diff --check`. |
| `T36-keelim-knowledge-vault-content-quality` | Aquinas | 19 selected ledger items verified with content-quality note expansion across Android, Kotlin, service, AI, Code, and Other domains, Bazel/Prototype naming fixes, Vault Log updates, backlink check for 251 files, targeted stale-marker scan over handled files, and `git diff --check`. |
| `T37-keelim-knowledge-vault-frontmatter` | Codex | 17 selected ledger items verified with a frontmatter role-field verifier, link regression verifier, script compile, backlink check, and `git diff --check`. |
| `T38-keelim-knowledge-vault-linking` | Codex | 6 selected ledger items verified with Knowledge Vault backlink checks, selected inbound/outbound wikilink checks, Python verifier compile, and `git diff --check`. |
| `T39-keelim-knowledge-vault-naming` | Kant | 21 selected ledger items verified with Knowledge Vault rename/link updates, backlink check for 251 files, JSON backlink check, old-basename audit, duplicate-basename audit leaving only `index.md`, and `git diff --check`. |
| `T40-keelim-knowledge-vault-structure` | Boole | 19 selected ledger items verified with local MOCs/schema navigation for AI, Android, CS, Kotlin, service, and vault-wide structures, Obsidian `.omx/` ignore, backlink JSON check returning ok with no failures, valid `.obsidian/app.json`, and `git diff --check`. |

## Ledger Commands

```sh
python3 scripts/improvements/init_progress_ledger.py --check
python3 scripts/improvements/init_progress_ledger.py --print-task-prompt T03-android-support-error-handling
python3 scripts/improvements/init_progress_ledger.py --set-task-status T01-android-support-ci-release assigned --owner Lovelace
python3 scripts/improvements/init_progress_ledger.py --set-item-status ASUP-001 verified --owner Lovelace --verification-command "cd android-support && bun run test" --verification-result "passed" --changed-file android-support/.github/workflows/test.yml
```

Use `assigned`, `in_progress`, `verified`, `blocked`, or
`needs_consumer_check` only when supported by evidence.
