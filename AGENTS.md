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
  - `docs/CODEMAPS/`
  - `docs/idea/`
  - `scripts/`
  - future `.gitmodules`
  - future root-only helper scripts/docs
- Do not convert child repositories to submodules yet while dirty or ahead-of-remote child repos remain unresolved.
- Do not discard, rewrite, or normalize child-repo changes from the root without an explicit request.

## Child repository autonomy
- Every top-level child directory (`all`, `all-web-ui`, `android-support`, `Keelim-Knowledge-Vault`, `keelim-plugin`, `keelim-vercel`, `quant`, `rich`, `toto`) remains its own Git repository and working context.
- When modifying code inside a child repo, enter that repo, use its own Git history, and follow any deeper `AGENTS.md` that applies there.
- Root-level changes should prefer updating documentation, submodule metadata, or pinned pointers rather than editing child-repo source files.
- A deeper `AGENTS.md` inside a child repo overrides this file for files under that child repo.
- Root `package.json` / `bun.lock` may act as a Bun workspace bootstrap for selected web repos, but this does **not** convert the root into a single Git monorepo or remove child-repo standalone responsibilities.
- A committed root Bun workspace may assume that autonomous child repos are already hydrated at their expected local paths; document that prerequisite in `README.md` whenever the workspace membership changes.

## Python uv workspace policy
- Root `pyproject.toml` / `uv.lock` may act as a uv workspace bootstrap for selected Python repos, but this does **not** convert the root into a single Python monorepo or remove child-repo standalone responsibilities.
- Keep uv workspace membership narrow and explicit. As of the initial uv bootstrap, the in-scope Python members are `toto` and `rich`; do not include sibling repos such as `../easy-release-note` unless explicitly requested.
- Do not change non-Python projects or existing Bun workspace behavior when doing uv workspace work.
- Use root `tool.uv.constraint-dependencies` for Python packages that should resolve consistently across workspace members. If a child repo directly declares a shared package, keep its child-local declaration aligned with the root constraint so standalone fallback installs remain honest.
- After uv dependency changes, run `uv run python scripts/verify-python-dependency-constraints.py`, `uv lock --check`, and package-local pytest commands documented in `README.md`. In sandboxed agent sessions, pass `--cache-dir .omx/uv-cache` if the default uv cache is not writable.

## Root idea backlog
- Workspace idea/backlog maintenance lives under `docs/idea/`.
- Do not recreate or maintain a root-level `idea/` directory; route the workspace index and per-project idea files to `docs/idea/index.md` and `docs/idea/<project>.md`.
- For idea gardener runs, read root `docs/CODEMAPS/*` first, then each project's `README.md` / `AGENTS.md` as read-only context before updating `docs/idea/`.
- Keep child repositories read-only during root idea maintenance unless the user explicitly asks to enter a child repo.

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

## Verification expectations for root changes
- For documentation/bootstrap work, verify the concrete files changed and report exact commands/results.
- Before root-level pinning, submodule, or workspace-boundary changes, run `bun run report:baseline` to capture the live child-repo registration/divergence state without mutating children.
- When touching the `all-web-ui` provider contract or its current consumers (`keelim-vercel`, `rich/web`), run `bun run report:shared-ui`; use `scripts/verify-all-web-ui-integration.sh` only when a strict static pass/fail gate is needed.
- When the root Git repository is initialized, prefer these checks after root-owned changes:
  - `git status --short`
  - `git status --ignore-submodules=none`
  - `git diff -- AGENTS.md README.md .gitignore .gitmodules`
- When root workspace metadata or helper scripts change, also run `bun run test` to keep the root contract scripts runnable.
- After submodules exist, also run:
  - `git submodule status`
  - `git ls-files --stage | grep 160000`

## Change boundaries
- Prefer the smallest reversible root diff.
- Prefer documentation over automation until the child-repo state is clean enough for safe submodule conversion.
- If a requested root change requires editing a child repo, call out the boundary explicitly and switch to that child repo's rules before changing it.
- For Bun workspace changes, prefer root bootstrap and metadata alignment before deeper package-boundary rewrites.
