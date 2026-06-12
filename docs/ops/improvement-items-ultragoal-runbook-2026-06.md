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
| `T05-android-support-testing` | Lovelace | `android-support` testing backlog |
| `T12-all-web-ui-testing` | Parfit | `all-web-ui` interaction/accessibility testing backlog |
| `T16-keelim-plugin-security` | Laplace | `keelim-plugin` security backlog |
| `T23-keelim-vercel-security` | Schrodinger | `keelim-vercel` security backlog |
| `T34-youtube-testing` | Erdos | `youtube` testing backlog |

## Verified Task Units

| task | worker | evidence |
|---|---|---|
| `T01-android-support-ci-release` | Lovelace | 19 selected ledger items verified with CI/release workflow checks, tests, coverage, build, bundle freshness, and `git diff --check`. |
| `T03-android-support-error-handling` | Lovelace | 18 selected ledger items verified with contextual error handling, retry/timeout guards, response validation, expanded tests, rebuilt bundle, and CI/release checks. |
| `T05-android-support-testing` | Lovelace | 18 selected ledger items verified with contract drift check, typecheck, test lint, unit tests, coverage, ncc build, CI/release workflow check, and `git diff --check`; leader rerun reported 9 suites / 144 tests / 100% coverage. |
| `T15-keelim-plugin-script-quality` | Laplace | 21 selected ledger items verified with Python compile checks, bundled script tests, skill verification, catalog check, SkillOpt validation, and `git diff --check`. |
| `T16-keelim-plugin-security` | Laplace | 17 selected ledger items verified with path/env guard changes, script/skill security regression tests, SkillOpt eval checks, skill/catalog checks, and leader rerun of `uv --cache-dir .skillopt/uv-cache run --python 3.12 python scripts/run-tests.py`. |
| `T18-keelim-plugin-testing-evals` | Laplace | 19 selected ledger items verified with repo-local test/eval runner, SkillOpt validation, score fixtures, skill/catalog checks, durable eval file visibility, and `git diff --check`. |
| `T20-keelim-vercel-api-correctness` | Schrodinger | 20 selected ledger items verified with authenticated API contracts, data envelopes, validation/error guards, CSV/SSRF limits, route tests, typecheck, build, maintenance check, and `git diff --check`. |
| `T35-keelim-knowledge-vault-automation` | Codex | 18 selected ledger items verified with vault-wide backlink JSON/file checks, resurface check/threshold behavior, schema/template contract checks, Obsidian properties/templates config checks, workspace cleanup checks, verifier compile, and `git diff --check`. |
| `T37-keelim-knowledge-vault-frontmatter` | Codex | 17 selected ledger items verified with a frontmatter role-field verifier, link regression verifier, script compile, backlink check, and `git diff --check`. |
| `T38-keelim-knowledge-vault-linking` | Codex | 6 selected ledger items verified with Knowledge Vault backlink checks, selected inbound/outbound wikilink checks, Python verifier compile, and `git diff --check`. |

## Ledger Commands

```sh
python3 scripts/improvements/init_progress_ledger.py --check
python3 scripts/improvements/init_progress_ledger.py --print-task-prompt T03-android-support-error-handling
python3 scripts/improvements/init_progress_ledger.py --set-task-status T01-android-support-ci-release assigned --owner Lovelace
python3 scripts/improvements/init_progress_ledger.py --set-item-status ASUP-001 verified --owner Lovelace --verification-command "cd android-support && bun run test" --verification-result "passed" --changed-file android-support/.github/workflows/test.yml
```

Use `assigned`, `in_progress`, `verified`, `blocked`, or
`needs_consumer_check` only when supported by evidence.
