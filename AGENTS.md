# keelim-maestro Root Superproject Guidance

## Intent
- This root directory is a coordination layer for multiple autonomous child Git repositories.
- The root repository manages workspace-level bootstrap files, later submodule metadata, and cross-repo operating guidance.
- Child repositories remain autonomous; do not treat this root as a monorepo that vendors their contents.

## Current safe scope
- Safe root-owned files:
  - `AGENTS.md`
  - `README.md`
  - `.gitignore`
  - `package.json`
  - `bun.lock`
  - `pyproject.toml`
  - `uv.lock`
  - `docs/CODEMAPS/`
  - `docs/ops/`
  - `docs/idea/`
  - `scripts/`
  - future `.gitmodules`
  - future root-only helper scripts/docs
- Do not convert child repositories to submodules yet while dirty or ahead-of-remote child repos remain unresolved.
- Do not discard, rewrite, or normalize child-repo changes from the root without an explicit request.

## Child repository autonomy
- Every top-level child directory (`all`, `all-web-ui`, `android-support`, `Keelim-Knowledge-Vault`, `keelim-plugin`, `keelim-vercel`, `quant`, `rich`, `youtube`) remains its own Git repository and working context.
- `/toto` is archived from the root coordination layer. If a local `toto/` checkout remains, treat it as an ignored historical checkout, not an active root submodule, workspace member, CodeGraph target, or backlog target.
- When modifying code inside a child repo, enter that repo, use its own Git history, and follow any deeper `AGENTS.md` that applies there.
- Root-level changes should prefer updating documentation, submodule metadata, or pinned pointers rather than editing child-repo source files.
- A deeper `AGENTS.md` inside a child repo overrides this file for files under that child repo.
- Root `package.json` / `bun.lock` may act as a Bun workspace bootstrap for selected web repos, but this does **not** convert the root into a single Git monorepo or remove child-repo standalone responsibilities.
- A committed root Bun workspace may assume that autonomous child repos are already hydrated at their expected local paths; document that prerequisite in `README.md` whenever the workspace membership changes.

## Python uv workspace policy
- Root `pyproject.toml` / `uv.lock` may act as a uv workspace bootstrap for selected Python repos, but this does **not** convert the root into a single Python monorepo or remove child-repo standalone responsibilities.
- Keep uv workspace membership narrow and explicit. After archiving `toto`, the in-scope Python members are `rich` and the private local `youtube` checkout; do not include sibling repos such as `../easy-release-note` unless explicitly requested.
- Keep `youtube/simple` outside the root uv workspace unless a later request explicitly promotes that nested Python project; it has its own lockfile and compatibility range.
- Do not change non-Python projects or existing Bun workspace behavior when doing uv workspace work.
- Use root `tool.uv.constraint-dependencies` for Python packages that should resolve consistently across workspace members. If a child repo directly declares a shared package, keep its child-local declaration aligned with the root constraint so standalone fallback installs remain honest.
- After uv dependency changes, run `uv run python scripts/verify-python-dependency-constraints.py`, `uv lock --check`, and package-local pytest commands documented in `README.md`. In sandboxed agent sessions, pass `--cache-dir .omx/uv-cache` if the default uv cache is not writable.

## Root idea backlog
- Workspace idea/backlog maintenance lives under `docs/idea/`.
- Do not recreate or maintain a root-level `idea/` directory; route the workspace index and per-project idea files to `docs/idea/index.md` and `docs/idea/<project>.md`.
- For idea gardener runs, read root `docs/CODEMAPS/*` first, then each project's `README.md` / `AGENTS.md` as read-only context before updating `docs/idea/`.
- Keep child repositories read-only during root idea maintenance unless the user explicitly asks to enter a child repo.

## CodeGraph boundaries
- Root and child repositories may each have their own `.codegraph/`, but choose the graph by question type.
- Prefer the root dispatcher for child code search: `bun run cg -- context <child-repo> "<task>"`, `bun run cg -- query <child-repo> <symbol>`, and `bun run cg -- files <child-repo> --max-depth 2`.
- The dispatcher lives at `scripts/codegraph.sh` and delegates to child `.codegraph/` indexes with CodeGraph `--path`; do not recreate a root aggregate graph for child implementation search.
- Use the root graph only for workspace maps, root-owned docs/scripts, shared config, and cross-project contract discovery.
- Use the target child repo graph as the primary source for implementation, bug impact analysis, call/symbol context, and test scope.
- Before using CodeGraph, check whether `.codegraph/` exists in both the root and the target child repo. If it is missing, report whether `codegraph init -i` is appropriate instead of initializing silently.
- Keep root CodeGraph coordination-only. The root `.gitignore` should exclude `.codegraph/`, child repo working trees, dependency folders, environment files, and generated output so the root index does not swallow child source trees.
- Sibling child repositories are read-only context unless the task explicitly requires them; explain the reason before editing across a child-repo boundary.
- See `docs/CODEMAPS/CODEGRAPH.md` for the reusable root-plus-subproject prompt contract and setup checklist.

## `/all-web-ui` policy
- `/all-web-ui` is currently treated as an autonomous local child repository from the root.
- It now has a remote-backed public repository, but root submodule expansion is still deferred until the remaining child-repo blockers are resolved.
- Include `/all-web-ui` in root-level subrepo status / verification helpers.
- Do not add `/all-web-ui` as a local-path submodule from the root.
- If it is later converted to a root submodule, use the remote-backed URL only after the broader workspace is safe to pin.
- It may participate in the root Bun workspace as a shared package, but it must remain independently cloneable/versionable for standalone consumer repos and Vercel builds.

## `/quant` policy
- `/quant` is intentionally excluded from the initial root superproject/submodule scope.
- Reason: `/quant` currently has no remote.
- Do not create a remote for `/quant` unless explicitly requested.
- Do not add `/quant` as a local-path submodule; that would break reproducible clone/bootstrap workflows.
- Keep `/quant` as an autonomous local repository unless a future explicit change request says otherwise.

## `/youtube` policy
- `/youtube` is a private autonomous child repository for YouTube Shorts and Easy Release Note production work.
- Include `/youtube` in root-level subrepo status / verification helpers.
- Do not add `/youtube` as a local-path submodule.
- `/youtube` participates in the root Bun workspace only through package paths declared in root `package.json` (`youtube/remotion`, `youtube/services/*`, and `youtube/videos/*`), not as an exact top-level Bun package.
- `/youtube` participates in the root uv workspace as the `easy-release-note` package; keep child-local dependency declarations aligned with root constraints so standalone fallback installs remain honest.
- If it later gets a private remote and is clean enough to pin, add it only through a remote-backed URL after the broader workspace blockers are resolved.

## `/toto` archive policy
- `/toto` is archived as of 2026-06-04 and should no longer receive root-level active handling.
- Do not add `/toto` back to `.gitmodules`, root Bun workspaces, root uv workspaces, CodeGraph dispatch, codemap refreshes, or idea gardener active project tables unless the user explicitly asks to reactivate it.
- Do not delete, reset, normalize, or rewrite a local `toto/` checkout from the root. The root `.gitignore` keeps `/toto/` ignored so any remaining checkout is operator-local historical context.

## Verification expectations for root changes
- For documentation/bootstrap work, verify the concrete files changed and report exact commands/results.
- Before root-level pinning, submodule, or workspace-boundary changes, run `bun run report:baseline` to capture the live child-repo registration/divergence state without mutating children.
- For child-repo status refresh or safe update previews, prefer `./scripts/update-subrepos.sh status` or `./scripts/update-subrepos.sh dry-run` before any manual multi-repo fetch/pull loop.
- When touching the `all-web-ui` provider contract or its current consumers (`keelim-vercel`, `rich/web`), run `bun run report:shared-ui`; use `scripts/verify-all-web-ui-integration.sh` only when a strict static pass/fail gate is needed.
- When the root Git repository is initialized, prefer these checks after root-owned changes:
  - `git status --short`
  - `git status --ignore-submodules=none`
  - `git diff -- AGENTS.md README.md .gitignore .gitmodules`
- When root workspace metadata or helper scripts change, also run `bun run test` to keep the root contract scripts runnable.
- After submodules exist, also run:
  - `git submodule status`
  - `git ls-files --stage | grep 160000`

## Root helper command boundaries
- `bun run cg`, `bun run cg:status`, and `bun run cg:root-check` are root-owned CodeGraph dispatch/inspection helpers; use them for coordination only and do not treat them as permission to initialize or rely on a root aggregate child-source graph.
- `bun run dev:keelim-vercel` and `bun run dev:rich-web` are root convenience wrappers for hydrated workspace members; they do not replace child-repo-local install, test, or release workflows.
- `bun run dev:codex-app-server` is the root helper for a local Codex app-server bound to this workspace; keep transport/config guidance at the root level rather than pushing it into child-repo docs.
- `bun run automation:local -- ...` is the root-owned local automation script index/delegator for `rich`, `youtube` n8n, and `tools/agentgateway`; keep runtime implementation, manifests, and secrets in the owning repos.
- `./scripts/update-subrepos.sh` is the root-owned status/update helper for registered submodules plus autonomous local repos surfaced in the report; prefer it over ad-hoc multi-repo pull loops when the task is root-level repo hygiene.
- `bun run dev:strategy-builder` and `bun run dev:backtester` are root convenience wrappers into `rich/open-trading-api/*`, but they do **not** make those nested apps root workspace members or change `rich`'s child-repo ownership rules.

## Change boundaries
- Prefer the smallest reversible root diff.
- Prefer documentation over automation until the child-repo state is clean enough for safe submodule conversion.
- If a requested root change requires editing a child repo, call out the boundary explicitly and switch to that child repo's rules before changing it.
- For Bun workspace changes, prefer root bootstrap and metadata alignment before deeper package-boundary rewrites.
