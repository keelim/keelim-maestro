# keelim-maestro Workspace Project Catalog

Use `docs/PROJECT.md` to assign ownership and locate every current project unit in
the workspace. Enter the owning repository before implementation and follow its
deepest applicable `AGENTS.md`.

This is a structural catalog, not a Git-status cache. The inventory is a
2026-08-30 working-tree snapshot. Reconfirm live registration, workspace
membership, and manifest contents before changing them. Entries marked
**working tree** are not yet durable repository structure.

## 1. Route the task

Assign every intended edit to exactly one owner before implementation.

| Request branch | Owner | Read next |
| --- | --- | --- |
| Root manifests, Git links, helper scripts, or workspace docs | `keelim-maestro` root | Root `AGENTS.md`, then the matching section below |
| Local MCP gateway, crawler services, or utility tooling | Autonomous `tools` checkout | `tools/README.md`, then the unit README or manifest |
| Android, Desktop/Wasm Compose, API schema, Rust native support, or iOS host work | `all` | `all/AGENTS.md`, then the deepest module guide |
| Shared React primitives and design tokens | `all-web-ui` | `all-web-ui/AGENTS.md` |
| Notes, PKM, and curated vault content | `Keelim-Knowledge-Vault` | Its `AGENTS.md` when present |
| Agent skills and plugin distribution | `keelim-plugin` | `keelim-plugin/AGENTS.md`, then the skill's `SKILL.md` |
| Vercel-hosted finance product and its Supabase resources | `keelim-vercel` | `keelim-vercel/AGENTS.md`, then the deepest guide |
| Market data, finance services, trading tools, or Rich admin UI | `rich` | `rich/AGENTS.md`, then the owning nested guide |
| YouTube, Shorts, Easy Release Note, or rendering services | `youtube` | `youtube/AGENTS.md`, then the package or video guide |
| Android release/support automation | `android-support` when present | The checkout's guides; report absence instead of inventing structure |
| Local quantitative experiments | `quant` only when explicitly requested and present | Its local guide; keep it outside root workspace and submodule changes |
| Archived `toto` work | No active owner | Require explicit reactivation before routing |

Completion criterion: every modified path has one declared owner,
cross-repository dependencies are ordered, and missing, archived, or
working-tree-only scopes are stated explicitly.

## 2. Use live authorities

| Question | Authority |
| --- | --- |
| Registered repositories, pins, branches, dirty state, and divergence | `bun run report:baseline` plus `.gitmodules` |
| Bun workspace membership | Root `package.json` |
| Python workspace membership and shared constraints | Root `pyproject.toml` and `uv.lock` |
| Gradle modules | `all/settings.gradle.kts` |
| A package's identity and commands | Its nearest `package.json`, `pyproject.toml`, `Cargo.toml`, `mix.exs`, `deno.json`, or build project |
| Root setup, automation, and operator workflows | The matching tracked section in root `README.md` |
| Repository shape when live discovery needs a map | `docs/CODEMAPS/README.md` and only the matching dated map, when present |

Treat codemaps, route counts, migration counts, and prose status tables as
snapshots. A live manifest or read-only report wins when they disagree.

## 3. Complete project inventory

Catalog rule: include each repository, package, application, deployable
function, registered build module, agent skill, and video production unit.
Shared-runtime features are listed but labeled as nested. Dependency trees,
caches, generated output, fixtures, migrations, routes, and script collections
are not separate projects.

### Root-owned units

| Path | Unit | Boundary and authority |
| --- | --- | --- |
| `./` | `keelim-maestro` coordination root | `.gitmodules`, `package.json`, `pyproject.toml`, and `scripts/`; it does not own child source |

`system/` currently contains only a working-tree debug artifact and owns no
project unit.

Root `docs/`, `scripts/`, `.agents/`, and `.claude/` belong to the coordination
root rather than separate products. `.omx/`, `.reports/`, `reports/`, `.tmp/`,
caches, virtual environments, and `node_modules/` are operational or generated
state.

### Autonomous `tools` checkout

`tools/` has its own Git root and is not tracked by the `keelim-maestro` root.
Keep its changes and status separate.

| Path | Unit | Boundary and authority |
| --- | --- | --- |
| `tools/` | Utility coordination repository | `tools/README.md` and its own Git status |
| `tools/agentgateway/` | Local MCP gateway runtime | Kubernetes resources rooted at `tools/agentgateway/k8s/kustomization.yaml` |
| `tools/crawler/` | `keelim-crawler` | Independent nested Git checkout, ignored by `tools`; Python CLI/server and its own operating guides; `tools/crawler/pyproject.toml` |
| `tools/crawler/web/` | `keelim-crawler-admin` | **Working tree, locally ignored** React/Vite application; `tools/crawler/web/package.json` |

`tools/codex-hygiene/` is a helper-script collection, not an independent
manifest project.

### `all`: product and platform builds

Primary registry: `all/settings.gradle.kts`. Its 37 registered Gradle modules
all have a local `build.gradle.kts` and `AGENTS.md`.

| Group | Count | Registered modules |
| --- | ---: | --- |
| Applications | 7 | `app-arducon`, `app-cnubus`, `app-my-grade`, `app-nanda`, `app-comssa`, `app-mysenior`, `composeApp` |
| Core | 15 | `core:common`, `core:common-android`, `core:component`, `core:designsystem`, `core:device-android`, `core:data`, `core:data-api`, `core:database`, `core:datastore-proto`, `core:domain`, `core:model`, `core:network`, `core:resource`, `core:testing`, `core:navigation` |
| Features | 11 | `feature:app-function`, `feature:settings-core`, `feature:settings-theme`, `feature:settings-notification`, `feature:settings-alarm`, `feature:settings-device`, `feature:settings-admin`, `feature:settings-lab`, `feature:ui-scheme`, `feature:ui-setting`, `feature:ui-web` |
| Other registered modules | 4 | `benchmarks`, `catalog`, `shared`, `widget` |

Four build units outside the 37-module registry are still part of `all`, for a
current total of 41 cataloged units:

- `build-logic/`: included Gradle convention-plugin composite build.
- `docs/`: private Bun/TypeSpec API-schema package rooted at `package.json`.
- `all-rust-lib/`: experimental Rust/JNI `cdylib` crate rooted at
  `Cargo.toml`; current Android loading integration must be verified before use.
- `allIos/`: tracked Xcode iOS shell rooted at `all.xcodeproj`; confirm its
  current Compose linkage before claiming it builds end to end.

Use `./gradlew projects` to refresh the registered Gradle list, then use the
owning module's guide for its checks. The TypeSpec, Rust, and iOS units follow
their own manifests rather than `settings.gradle.kts`.

### `all-web-ui` and `Keelim-Knowledge-Vault`

| Repository | Current units | Boundary |
| --- | --- | --- |
| `all-web-ui` | One publishable package: `@keelim/all-web-ui` | `all-web-ui/package.json`; components and exports are one package, not nested projects |
| `Keelim-Knowledge-Vault` | One content repository | No nested build/run manifest in the current checkout; vault folders are content areas |

`all-web-ui/.ds-sync/` is an ignored generated dependency workspace, not a
second package.

For provider or consumer contract changes, inspect with
`bun run report:shared-ui` and verify the provider plus affected consumers.

### `keelim-plugin`: 11 skill units

Each directory below is routed through its own `SKILL.md`:

- `agent-instructions-improver`
- `codebase-codemap`
- `codex-insights`
- `easy-release-note-video-pipeline`
- `eav` (**working tree**)
- `eli5` (**working tree**)
- `html-report-generator`
- `jira-ticket-desk`
- `release-automation`
- `session-usage-dashboard`
- `tech-post-maker`

Refresh the list from `keelim-plugin/skills/*/SKILL.md`. Validate changes with
the repository's catalog generator and `scripts/verify-skills.sh` flow.

### `keelim-vercel`: application and deployable functions

| Unit | Boundary |
| --- | --- |
| `keelim-vercel` | One Next.js application rooted at `keelim-vercel/package.json` |
| `crawl-sectors` | Supabase Edge Function at `supabase/functions/crawl-sectors/` |
| `send-newsletter` | Supabase Edge Function at `supabase/functions/send-newsletter/` |

The current application snapshot contains 112 dashboard pages, 8 other pages,
18 API routes, and 14 SQL migrations. They are surfaces of the application,
not separate projects. Use `bun run verify:maintenance`; add
`bun run typecheck:supabase` or `bun run db:check` when those boundaries change.

### `rich`: six active execution units

| Unit | Boundary | Read or verify |
| --- | --- | --- |
| Rich Python backend | `rich/pyproject.toml`, FastAPI entry at `app/main.py` | `rich/AGENTS.md`; `bun run python:check` |
| Rich Admin Web | `rich/web/package.json` | Test, typecheck, and build from `rich/web` |
| `crawl-sectors` | `rich/supabase/functions/crawl-sectors/deno.json` | Function README and Deno checks |
| `crawl-housing-notices` | `rich/supabase/functions/crawl-housing-notices/deno.json` | `rich/docs/housing-notice-api-contract.md` and function checks |
| `slack-review-reminder` | `rich/supabase/functions/slack-review-reminder/deno.json` | Function README and Deno checks |
| Symphony | `rich/symphony/mix.exs` | `symphony/AGENTS.md`, then `mix test` |

`rich/package.json` is a command coordinator rather than a seventh product.
`rich/open-trading-api/requirements.txt` is a legacy pin list; the owning Python
dependency authority remains `rich/pyproject.toml` and `rich/uv.lock`.
The Open Trading code is integrated into the Python backend and Admin Web. It
has no independent nested application manifest, but it contains five routed
feature units:

1. Unified Open Trading FastAPI routes.
2. Strategy Builder.
3. Backtester and the `kis_backtest` library.
4. KIS Backtest MCP server.
5. Lean/KIS data-preparation automation.

Read `rich/docs/open-trading-runtime-contract.md`, then
`rich/open-trading-api/README.md` and the matching builder/backtester README.
The Backtester tests live outside Rich's default `tests/` scope and must be
named explicitly when Open Trading changes.

Supabase migrations, SQL tests, tracked operational scripts, the local
Kubernetes lane, and the market-snapshot cron installer support these units;
they are not additional projects. `rich/TradingAgents/` is an ignored external
checkout, not a Rich-owned subproject. Ignore `symphony/deps/`, `web/.next/`,
`.lean-workspace/`, `.master/`, and cache/generated directories.

### `youtube`: four tool/service packages, eight video units, and one local runtime

Tool and service packages:

| Unit | Boundary |
| --- | --- |
| `easy-release-note` | Python package and `ern` CLI at `youtube/pyproject.toml` |
| `easy-release-note-remotion` | Shared renderer at `youtube/remotion/package.json` |
| `ai-content-generator-service` | `youtube/services/ai-content-generator/package.json` |
| `remotion-template-admin` | `youtube/services/remotion-template-admin/package.json` |

Current video production units are a **2026-08-30 working-tree snapshot**:

| Engine | Video units |
| --- | --- |
| HyperFrames | `chatgpt-chrome-extension-paper-cut-en`, `chatgpt-chrome-extension-paper-cut-ko`, `chatgpt-desktop-codex-workspace-en`, `chatgpt-desktop-codex-workspace-ko` |
| Remotion | `chatgpt-computer-history`, `chatgpt-desktop-codex`, `claude-tag-slack-beta`, `microsoft-intelligent-terminal` |

HyperFrames units are identified by `videos/<slug>/hyperframes.json`; Remotion
units by `videos/<slug>/remotion/episode*.json`, with `episodes/*.json` as the
production registry. These eight directories are currently untracked and must
not be described as committed structure. `youtube/simple` is absent. Validate a
video with `uv run ern render <slug>` and `uv run ern validate <slug>`; upload
inspection uses `uv run ern upload --dry-run <slug>`.

The tracked `youtube/ops/n8n-k8s/` manifests define one local Kubernetes n8n
runtime with task runners. The two workflow JSON files under
`youtube/ops/n8n/workflows/` support that runtime and are not additional
projects. Route its lifecycle through the root `README.md` local-automation
flow and the owning `youtube` guidance.

## 4. Absent, archived, and excluded paths

| Path | Current treatment |
| --- | --- |
| `android-support/` | Absent and not registered in `.gitmodules`; route only after a checkout is explicitly restored |
| `quant/` | Absent in this checkout and excluded by root policy; do not create a remote or workspace entry implicitly |
| `toto/` | Archived and absent; any future local checkout remains historical until explicit reactivation |
| `system/` | Working-tree artifact folder with no project manifest |
| `keelim-plugin/.skillopt/SkillOpt/` | Ignored cache clone; never catalog as a workspace project |
| `rich/TradingAgents/` | Ignored optional external checkout; not owned by the Rich manifest set |

## 5. Work and verification gates

1. Enter the declared owner and read the deepest applicable `AGENTS.md` before
   editing.
2. Keep sibling repositories read-only unless the request explicitly spans
   them. Preserve unrelated dirty changes.
3. Use live manifests for membership. Label working-tree-only structures and
   dated counts instead of presenting them as durable facts.
4. Run the owning project's documented checks. For a cross-repository change,
   verify every owner and use the changeset-manifest flow in root `README.md`
   when delivery order matters.
5. For root documentation, run `git diff --check`, a path-scoped `git diff`,
   and both normal and submodule-aware status views.

Catalog refresh is complete only when every current manifest/build registry
unit appears exactly once, nested shared-runtime features are not presented as
independent apps, missing or archived paths are explicit, generated/cache
trees are excluded, and every changed file plus verification result is
reported.

## Authority order

Resolve conflicts in this order: the user's explicit scope, the deepest
applicable `AGENTS.md`, live manifests and read-only reports, dated reference
documents, then this catalog. This file chooses where to work; it does not
override an owning repository's rules.
