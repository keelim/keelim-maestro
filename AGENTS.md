# keelim-maestro working guide

This repository coordinates child ownership, shared development setup, and verification across independent Git repositories. It serves operators and agents working across those projects; it does not merge their source, history, or deployment boundaries.

## Project structure

```text
./
├── AGENTS.md                              → Shared entry point
├── CLAUDE.md                              → Link to the same guide
├── scripts/
│   ├── AGENTS.md                           → Shared helper command rules
│   └── improvements/AGENTS.md              → Research input and output boundaries
└── .agents/skills/
    ├── maestro-orchestrator/AGENTS.md      → Owner assignment and result integration
    └── boundary-check/AGENTS.md            → Read-only boundary review
```

## Hard gates

1. Assign each changed path to an owner and preserve unrelated edits, staged content, and local commits. Do not reset or normalize child repositories from the root.
2. Keep package membership distinct from Git ownership. A helper command or nested folder does not authorize adding a workspace member or submodule.
3. Stay within the request for publication, deployment, credential changes, and destructive actions. Never put secrets in source or reports.
4. Check optional repository existence. Reactivating archived `toto` or changing `quant` remotes/registration requires a separate request.
5. Separate implementation, static checks, runtime checks, and external-service verification. Root checks and connection indicators do not certify child products.
6. `rich` is local-only under `scripts/repository-policy.sh`: no remote or upstream is normal. Preserve its Bun/Python membership, local work, and runtimes; exclude it from GitHub PR collection/creation and fetch/pull/push automation, including explicit GitHub URLs. Reconnecting it requires a separate request.

## Before work

- For root or cross-repository work, use the ownership inventory in README.md and read the guide closest to the changed area. When the local documentation archive is available, consult its project catalog, change standards, and engineering notes.
- Before membership, gitlink, or pin changes, inspect live declarations and run `bun run report:baseline`. Afterward compare `git submodule status` and gitlinks.
- For shared UI, read the provider and consumer contracts in `all-web-ui`, `keelim-vercel`, and `rich/web`; use `bun run report:shared-ui` to scope verification.
- Before runtime, authentication, or knowledge-input work, read the owner’s security and operating instructions and confirm the destination. Python and Bun changes must not expand one another’s membership implicitly.
- Use the owning codebase-memory index and scoped text search for structure. Optional codemaps and dated research live in the local documentation archive described in README.md; do not recreate a repository documentation directory.

## Problem routing

Stop the affected action and immediately report lost work, unauthorized child changes, exposed secrets, writes to an unconfirmed database, or concurrent PGLite access that could corrupt the store. Record other unresolved issues, reproduction conditions, impact, and the reason they remain unresolved in the owner’s issue log or the local documentation archive. Fix in-scope defects that can be resolved now and report the actual check results.
