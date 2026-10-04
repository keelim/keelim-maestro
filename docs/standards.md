# Change and verification standards

## Ownership

Assign every changed path to its owner. Root scope includes entry guides, README, project catalog, root configuration and lockfiles, `scripts/`, workspace documentation, and the two shared skills. Product implementation follows the deepest guide in its own repository.

Preserve unrelated edits, staged changes, and local commits. Do not initialize or normalize child repositories during root work. Keep `all-web-ui` and `youtube` autonomous. Do not register a submodule using a local path as if it were a reproducible remote. New pins require a confirmed remote, worktree/history inspection, and a reproducible clone path.

Check optional checkout existence first. Exclude `toto` until explicitly reactivated; do not implicitly create a remote or registration for `quant`.

## Dependencies and execution

Use root `package.json` for Bun membership and `pyproject.toml` for Python membership. Neither nesting nor a helper command creates membership. Workspaces coordinate installation without changing Git ownership. Keep shared Python constraints and each child's direct dependencies and independent installation contract consistent.

Do not combine unrelated Bun behavior changes with Python dependency work. Membership changes update the manifest, lockfile, and bootstrap instructions together. Delegate installation, checking, and release to the owner; do not copy product implementations or secret configuration into root helpers.

Use `.gitmodules` and gitlinks for registration, `mise.toml` for tool versions, and owner manifests for package contents. Historical tables must not override them.

## Required evidence

| Change | Required checks |
| --- | --- |
| Root documentation or bootstrap instructions | Review changed files; `git diff --check`, `git status --short`, `git status --ignore-submodules=none` |
| Root helpers or workspace configuration | The above plus `bun run test` |
| Membership, pins, or submodules | Before: `bun run report:baseline`; after: `git submodule status` and gitlinks from `git ls-files --stage` |
| Shared UI provider/consumer contract | `bun run report:shared-ui`, affected owner checks, and strict static `sh scripts/verify-all-web-ui-integration.sh` |
| Python dependencies | `uv run python scripts/verify-python-dependency-constraints.py`, `uv lock --check`, and explicit affected pytest paths |
| Agent guides or shared skills | Relative paths, link targets, metadata, effective instruction chains, and the default 32 KiB budget |

Separate static, runtime, external-service, and visual verification. Environment or authentication blockers are not passing checks. File inspection does not prove that an existing agent reloaded instructions; that requires a new-session check.

## Exploration and durable guidance

Prefer the owning codebase-memory index for structural questions; use text search for configuration, prose, literals, and missing coverage. Do not create one root index containing child sources. The CodeGraph dispatcher selects existing child indexes and must not silently initialize missing ones.

Keep ideas in `docs/idea/`, cross-project research in `docs/research/`, and operator knowledge material in `docs/knowledge/`. Preserve existing records. Validate research paths, line ranges, unique IDs, required fields, and output constraints such as no URLs. Do not put session IDs, debug logs, or temporary paths in permanent guidance.

Keep durable rules in the closest owning `AGENTS.md` and detailed procedures/examples in that area's documents. Do not duplicate source-derived inventories as permanent rules.

## Collaboration

Workers own nonoverlapping paths and preserve others' changes. Use EAV for code work unless the user chooses another procedure. Do not create user-owned chats for implementation subtasks. If delegation is unavailable, work sequentially with the same ownership and verification rules.

Create `_workspace/<unique-run-id>/` only when a saved handoff is necessary; never reuse or overwrite another run's records. Keep shared skill sources in `.agents/skills` and Claude compatibility paths linked to them.

Use a separate Claude process for an explicit Claude/Fable request, another-model review, or bounded delegation. Preserve discovery and permissions. If authentication, model, MCP, or JSON errors persist after one safe retry, report the cause and stopped state. Do not add commits, branch changes, or deployment to a task without authorization.
