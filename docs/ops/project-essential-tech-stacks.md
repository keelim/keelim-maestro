# Project Essential Tech Stacks

Generated on 2026-06-07 from the root superproject, child `AGENTS.md` files,
README files, manifests, and `docs/CODEMAPS/projects/*` snapshots.

This is an architecture-oriented stack review. "Essential" means removing the
stack would break the project's current ownership model, runtime contract,
verification path, or deployment shape. It does not list every library.

## Scope

Active project surfaces in the current root checkout:

| Surface | Root relationship | Include in this review |
| --- | --- | --- |
| `keelim-maestro` | root coordination repo | yes |
| `all` | registered gitlink/submodule path | yes |
| `android-support` | registered gitlink/submodule path | yes |
| `Keelim-Knowledge-Vault` | registered gitlink/submodule path | yes |
| `keelim-plugin` | registered gitlink/submodule path | yes |
| `keelim-vercel` | registered gitlink/submodule path | yes |
| `all-web-ui` | autonomous local repo, root Bun workspace member | yes |
| `rich` | autonomous local repo, root Bun and uv workspace member | yes |
| `youtube` | private autonomous local repo, root Bun and uv workspace member | yes |
| `tools` | ignored local tools repo | supporting ops only |
| `quant` | policy mentions it, but this checkout currently lacks the path | no live stack evidence |
| `toto` | archived local checkout | excluded unless explicitly reactivated |

## Cross-Project Baseline

The root should not become a single merged monorepo. The essential cross-project
stack is a coordination stack:

| Layer | Essential stack | Why it matters |
| --- | --- | --- |
| Repo boundaries | Git submodules/gitlinks for registered repos, autonomous local repos for `all-web-ui`, `rich`, `youtube` | Keeps child repos independently versioned and prevents root-level edits from swallowing child source. |
| JS workspace bootstrap | Bun 1.3, root workspaces for shared web members, root catalog pins | Coordinates installs and shared React/Next/Tailwind versions without changing child Git ownership. |
| Python workspace bootstrap | uv, Python 3.13 root resolver, `rich` + `youtube` workspace members, root constraint dependencies | Keeps shared Python dependency resolution consistent while preserving child-local fallback. |
| Shared UI contract | `@keelim/all-web-ui`, GitHub Packages, root `report:shared-ui` | Prevents duplicated shadcn primitives and keeps `keelim-vercel` plus `rich/web` on one UI provider contract. |
| Local automation | `scripts/local-automation.sh`, `tools/agentgateway`, Kubernetes port-forward contract | Keeps MCP and local runtimes behind root-owned coordination instead of scattered ad hoc commands. |
| CodeGraph/codemaps | root dispatcher plus child `.codegraph/` and `docs/CODEMAPS/projects/*` | Maintains architecture search by repo boundary, not by aggregate root source scan. |

## Project Stack Matrix

### `all`

Role: multi-app Android/Kotlin workspace.

Essential stack:

- Kotlin, Android Gradle Plugin, Gradle version catalog, custom convention plugins.
- Jetpack Compose and Material 3 for UI.
- Hilt for dependency injection.
- Room and DataStore for persistence.
- Kotlin coroutines, Flow/StateFlow, MVVM plus UDF state model.
- Multi-module Android architecture: `app-*`, `feature/*`, `core/*`, `shared/`.
- Kotlin Multiplatform only where shared code is already part of the project.
- JVM 17 target, min SDK 26, current Android target API.
- Gradle tests, module-boundary checks, and scoped JaCoCo coverage tasks.

Architecture requirement:

Keep app code flowing through `app-* -> feature:* -> core:*` boundaries. Do not
let feature modules depend on `core:data` implementation internals when a
`core:data-api` boundary exists. Keep Android-only dependencies out of
`commonMain`.

Optional or bounded stack:

- Rust/Cargo under `all-rust-lib` is a bounded support surface, not the default
  application stack.
- Kotlin/JS or generated WASM package artifacts should stay secondary unless a
  feature explicitly owns them.

### `all-web-ui`

Role: shared React primitive and design-token package for Keelim web apps.

Essential stack:

- Bun package workflow.
- TypeScript and React 19.
- Radix/shadcn-compatible primitives.
- Tailwind CSS 4, semantic CSS variables, and `--kui-*` design tokens.
- `src/index.ts`, `src/manifest.ts`, package subpath exports, and generated
  `dist/` output.
- `DESIGN.md` as the canonical design-system source, plus Stitch metadata as
  design workflow evidence.
- Bun tests, typecheck, build, and design.md lint when design tokens change.

Architecture requirement:

This package owns reusable primitives and theme contracts only. It should not
grow app routes, product flows, or consumer-specific feature logic. Consumer
repos should import scoped exports such as `@keelim/all-web-ui/button` and keep
local `components/ui/*` files as shims or app-specific composites.

Optional or bounded stack:

- Stitch and design.md tools are essential when changing design-system source,
  but not needed for every primitive-only bug fix.

### `android-support`

Role: GitHub Action for signing and uploading Android APK/AAB releases to Google
Play.

Essential stack:

- Node/TypeScript action code.
- Bun as package manager.
- `@actions/*` GitHub Action runtime packages.
- `@googleapis/androidpublisher` and Google Play Developer API v3.
- `@vercel/ncc` compiled `lib/index.js`, committed for action execution.
- Jest plus `ts-jest` for tests.
- Android SDK build-tools for signing: `zipalign`, `apksigner`, and `jarsigner`.
- `action.yml` input/output contract and multi-file `releaseFiles` handling.

Architecture requirement:

Treat this as an action artifact, not a general app. Source lives in `src/`,
compiled action output lives in `lib/`, and API behavior must be driven through
the action input contract. `releaseFile` is deprecated; `releaseFiles` is the
durable input.

Optional or bounded stack:

- Manual build workflow scripting is support tooling, not the core architecture.

### `Keelim-Knowledge-Vault`

Role: Obsidian-style LLM wiki and personal knowledge vault.

Essential stack:

- Markdown as the primary data format.
- Obsidian-style `[[wikilinks]]`.
- Domain hubs and topic notes.
- Vault schema docs under `schema/`.
- `ops/domain-map.md` for loose-note routing.
- Korean note titles and path-qualified links where basename collisions exist.

Architecture requirement:

This is not an app runtime. The architecture is an information architecture:
input source material becomes durable notes, notes connect through hubs, and
answers that should compound are written back into the vault. Avoid bulk note
moves before hub links and domain ownership are clear.

Optional or bounded stack:

- Backlink/lint scripts are useful verification helpers, but Markdown schema and
  link discipline are the essential stack.

### `keelim-plugin`

Role: reusable local skill collection for Codex and Claude.

Essential stack:

- Skill folders under `skills/<skill-name>/`.
- `SKILL.md` with frontmatter as the source of truth.
- Optional `agents/openai.yaml` for Codex UI metadata.
- Python 3.12 via uv for repo-local scripts and SkillOpt/promotion tooling.
- YAML/Markdown/JSON conventions for skill metadata.
- Deterministic promotion scripts and smoke validation for skill changes.

Architecture requirement:

Keep this repo as a docs-first skill collection. Automation scripts should
support skill quality, promotion, validation, or installation. Do not store
secrets, session logs, one-off task state, or unrelated workspace maintenance in
skill files.

Optional or bounded stack:

- SkillOpt is an optimization pipeline, not required for every skill edit.
- `npx skills add` is an installation path, not the internal source format.

### `keelim-vercel`

Role: standalone Vercel-deployed Korean financial toolkit.

Essential stack:

- Bun package workflow.
- Next.js App Router, React 19, TypeScript strict mode.
- Tailwind CSS 4 and shadcn/Radix-compatible UI through `@keelim/all-web-ui`.
- LocalStorage as primary client persistence for many tools.
- Supabase for newsletter, forex, notices, and other server-backed flows.
- NextAuth v5/GitHub OAuth where auth is required.
- Vercel deployment, Vercel Analytics, and Speed Insights.
- SEO metadata, sitemap/robots, JSON-LD, and OG route behavior.
- Bun tests, ESLint, TypeScript typecheck, and maintenance verifiers.

Architecture requirement:

Keep standalone Vercel clone/build behavior intact. Do not leave parent-workspace
only dependency protocols such as `catalog:` or `workspace:*` in the standalone
consumer manifest. Shared primitives should enter through scoped
`@keelim/all-web-ui/*` exports and the adapter boundary, not new independent
generic `components/ui/*` implementations.

Optional or bounded stack:

- Finance API libraries such as Yahoo Finance and chart libraries are feature
  dependencies. They are essential only for the routes that use them.
- Recharts must remain dynamically imported where the project guide requires it
  for SSR stability.

### `rich`

Role: local admin and finance/market operations workspace.

Essential stack:

- Python 3.13, uv, FastAPI, Uvicorn.
- Supabase Postgres, Storage, RLS, service-role backend access, and Supabase
  Edge Functions.
- PyKRX/KRX, OpenDART, and KIS/Open Trading integrations for Korean market and
  strategy flows.
- Next.js App Router, React 19, TypeScript, Tailwind CSS, React Query, and
  Supabase SSR/browser clients under `web/`.
- Bun root workspace resolution for `rich/web` catalog dependencies.
- Deno/Bun tests for Supabase edge-function code.
- Local Kubernetes/Skaffold/Docker for the heavier backend/frontend dev loop.
- Google OAuth/Calendar/Sheets flows where agenda and related admin pages need
  them.

Architecture requirement:

Keep the split clear:

- FastAPI owns privileged aggregation, read-only market APIs, service-role
  Supabase operations, Open Trading backend routes, and source/failure semantics.
- Next.js owns the admin UI, session-aware browser/server Supabase clients, and
  feature hooks.
- Supabase owns persisted data, RLS, storage, edge automations, and cron-backed
  jobs.

Page-load flows should not silently mutate financial source data. KRX/KIS/DART
features need explicit source availability semantics, not cache-vs-empty
confusion.

Optional or bounded stack:

- Kubernetes/Skaffold is a local heavy dev loop; process-based FastAPI plus
  Next.js remains the lightweight default path.
- Historical Open Trading standalone frontend folders are not normal root
  workspace members after integration into `rich/web`.

### `youtube`

Role: private Easy Release Note YouTube Shorts production repo.

Essential stack:

- Python 3.11 child-local CLI package, coordinated by root uv when used from
  `keelim-maestro`.
- `uv run ern ...` CLI for scaffold, render, validate, chart-race, stock-price,
  and upload dry-run workflows.
- Remotion, React, TypeScript, and Bun package paths under `remotion/`,
  `services/*`, and `videos/*`.
- Structured production artifacts: `episodes/`, `packages/`, `videos/<slug>/`,
  and `renders/`.
- Source-first package evidence: official source URLs, access dates, scripts,
  visual plans, metadata, and verification notes.
- Shorts media constraints: vertical MP4, H.264/AAC, 1080 x 1920, safe-area
  discipline, ffmpeg/ffprobe validation.
- Bilingual English/Korean output sets by default for public motion-graphic
  video assets.
- Optional downstream upload surfaces such as YouTube Studio, Google Vids, and
  Naver Clip only after explicit publishing or handoff scope.

Architecture requirement:

The production unit is a source-backed package plus renderable episode JSON, not
just an MP4. Remotion is the default scalable renderer for new repeatable
episodes, while HyperFrames can remain for custom HTML/GSAP compositions. Keep
`youtube` private and autonomous: do not add a top-level `youtube/package.json`
or root submodule entry just to satisfy workspace tooling.

Optional or bounded stack:

- HyperFrames, Google Vids, TTS, and upload automation are downstream production
  lanes. They are essential only when that episode or task explicitly chooses
  them.
- Naver Clip limits and YouTube/Shorts policy details can change; verify current
  platform rules before final registration.

### `tools`

Role: local-only machine tools around the workspace, not a root-owned active
child project.

Essential stack when used:

- `tools/agentgateway`: Kubernetes, Docker image build context, MCP HTTP
  gateway, `kubectl` port-forward to `localhost:3000` and admin UI on `15000`.
- `tools/crawler`: Python 3.10, uv, Crawl4AI, Playwright browser control,
  FastAPI/Uvicorn, SQLite-oriented collector outputs.
- `tools/crawler/web`: React/Vite/TypeScript/Vitest admin UI when the crawler
  dashboard is in scope.

Architecture requirement:

Treat `/tools` as local-only unless a remote and root policy explicitly change.
Secrets, logs, generated browser output, and runtime files stay out of git.

Open check:

- `tools/crawler/README.md` says the React admin app is registered in the root
  Bun workspace as `keelim-crawler-admin`, but the current root `package.json`
  workspace list does not include `tools/crawler/web`. Treat that as unresolved
  local tooling documentation until reconciled.

## Architecture Review Summary

1. The workspace has three durable stack families: Android/Kotlin mobile
   (`all`), web/React/Next shared surfaces (`all-web-ui`, `keelim-vercel`,
   `rich/web`, `youtube/remotion`), and Python/uv service or production
   pipelines (`rich`, `youtube`, `keelim-plugin`, `tools/crawler`).
2. The root's most important architectural job is boundary preservation:
   submodule paths, autonomous repos, Bun workspace members, and uv workspace
   members are related but not identical ownership models.
3. Shared UI should remain centralized in `all-web-ui`; consumer apps should not
   recreate generic primitives.
4. Financial data projects need source-boundary language as part of the stack:
   KRX/KIS/OpenDART/Supabase are not interchangeable caches.
5. `youtube` should be treated as a production pipeline. The essential stack is
   source package -> episode JSON -> renderer -> validation -> handoff, not only
   Remotion or a video file.
6. `quant` has no live checkout evidence here; keep it out of stack decisions
   until the path exists or the user provides the repo.
7. `toto` remains archived and should not influence active stack choices.

## Evidence Sources

- Root boundary and workspace policy: `AGENTS.md`, `README.md`, `package.json`,
  `pyproject.toml`, `.gitmodules`.
- Existing codemap snapshots: `docs/CODEMAPS/keelim-maestro.md`,
  `docs/CODEMAPS/projects/*.md`.
- `all`: `all/AGENTS.md`, `all/settings.gradle.kts`,
  `all/build.gradle.kts`, `all/gradle/libs.versions.toml`,
  `all/docs/architecture/*`.
- `all-web-ui`: `all-web-ui/AGENTS.md`, `all-web-ui/README.md`,
  `all-web-ui/package.json`, `all-web-ui/DESIGN.md`,
  `all-web-ui/tests/components.test.tsx`.
- `android-support`: `android-support/AGENTS.md`,
  `android-support/README.md`, `android-support/package.json`,
  `android-support/src/*`, `android-support/__tests__/*`.
- `Keelim-Knowledge-Vault`: `Keelim-Knowledge-Vault/AGENTS.md`,
  `Keelim-Knowledge-Vault/README.md`,
  `Keelim-Knowledge-Vault/schema/*`,
  `Keelim-Knowledge-Vault/ops/domain-map.md`.
- `keelim-plugin`: `keelim-plugin/AGENTS.md`, `keelim-plugin/README.md`,
  `keelim-plugin/pyproject.toml`, `keelim-plugin/skills/*`.
- `keelim-vercel`: `keelim-vercel/AGENTS.md`,
  `keelim-vercel/README.md`, `keelim-vercel/package.json`,
  `keelim-vercel/next.config.js`.
- `rich`: `rich/AGENTS.md`, `rich/README.md`, `rich/package.json`,
  `rich/pyproject.toml`, `rich/web/package.json`, `rich/supabase/config.toml`,
  `rich/docs/CODEMAPS/*`.
- `youtube`: `youtube/AGENTS.md`, `youtube/README.md`,
  `youtube/pyproject.toml`, `youtube/remotion/package.json`,
  `youtube/services/*/package.json`, `youtube/videos/*/package.json`.
- `tools`: `tools/README.md`, `tools/agentgateway/README.md`,
  `tools/crawler/README.md`, `tools/crawler/pyproject.toml`,
  `tools/crawler/web/package.json`.
