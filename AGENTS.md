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
  - future `.gitmodules`
  - future root-only helper scripts/docs
- Do not convert child repositories to submodules yet while dirty or ahead-of-remote child repos remain unresolved.
- Do not discard, rewrite, or normalize child-repo changes from the root without an explicit request.

## Child repository autonomy
- Every top-level child directory (`all`, `all-web-ui`, `android-support`, `c2g-proxy`, `Keelim-Knowledge-Vault`, `keelim-plugin`, `keelim-vercel`, `quant`, `rich`) remains its own Git repository and working context.
- When modifying code inside a child repo, enter that repo, use its own Git history, and follow any deeper `AGENTS.md` that applies there.
- Root-level changes should prefer updating documentation, submodule metadata, or pinned pointers rather than editing child-repo source files.
- A deeper `AGENTS.md` inside a child repo overrides this file for files under that child repo.

## `/c2g-proxy` policy
- `/c2g-proxy` is a GitHub-backed registered root submodule.
- It is the workspace home for the Claude Code + LiteLLM + Gemini bridge artifacts.
- When updating it from the root, pin it via the remote-backed submodule entry and verify with `git submodule status`.

## `/all-web-ui` policy
- `/all-web-ui` is currently treated as an autonomous local child repository from the root.
- It now has a remote-backed public repository, but root submodule expansion is still deferred until the remaining child-repo blockers are resolved.
- Include `/all-web-ui` in root-level subrepo status / verification helpers.
- Do not add `/all-web-ui` as a local-path submodule from the root.
- If it is later converted to a root submodule, use the remote-backed URL only after the broader workspace is safe to pin.

## `/quant` policy
- `/quant` is intentionally excluded from the initial root superproject/submodule scope.
- Reason: `/quant` currently has no remote.
- Do not create a remote for `/quant` unless explicitly requested.
- Do not add `/quant` as a local-path submodule; that would break reproducible clone/bootstrap workflows.
- Keep `/quant` as an autonomous local repository unless a future explicit change request says otherwise.

## Verification expectations for root changes
- For documentation/bootstrap work, verify the concrete files changed and report exact commands/results.
- When the root Git repository is initialized, prefer these checks after root-owned changes:
  - `git status --short`
  - `git status --ignore-submodules=none`
  - `git diff -- AGENTS.md README.md .gitignore .gitmodules`
- After submodules exist, also run:
  - `git submodule status`
  - `git ls-files --stage | grep 160000`

## Change boundaries
- Prefer the smallest reversible root diff.
- Prefer documentation over automation until the child-repo state is clean enough for safe submodule conversion.
- If a requested root change requires editing a child repo, call out the boundary explicitly and switch to that child repo's rules before changing it.
