# keelim-maestro working guide

This repository coordinates child ownership, shared development setup, and verification across independent Git repositories. It serves operators and agents working across those projects; it does not merge their source, history, or deployment boundaries.

## Project structure

```text
./
├── AGENTS.md                              → Shared entry point
├── CLAUDE.md                              → Link to the same guide
├── docs/
│   ├── PROJECT.md                         → Owner routing and project inventory
│   ├── architecture.md                    → Components and dependency direction
│   ├── business-rules.md                  → Ownership, updates, and completion
│   ├── security.md                        → Access and protected assets
│   ├── standards.md                       → Complete change and verification rules
│   ├── engineering-notes.md                → Operational traps and diagnosis
│   ├── operations.md                       → Setup, execution, and checks
│   ├── contracts.md                        → Command inputs, outputs, and failures
│   ├── tracking/
│   │   ├── status.md                       → Capabilities, evidence, and remaining conditions
│   │   ├── findings.md                     → Unresolved problems
│   │   └── decisions/
│   │       ├── index.md                    → Decision index
│   │       ├── 0001-independent-repositories.md → Independent child ownership
│   │       ├── 0002-scoped-workspaces.md        → Selected installation membership
│   │       ├── 0003-observe-before-mutate.md    → Separate inspection and updates
│   │       ├── 0004-separate-knowledge-store.md → Separate operator knowledge store
│   │       └── 0005-remove-root-chart.md       → Remove the root video generator
│   └── videos/subproject-intros/AGENTS.md   → Intro-video editing boundary
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

## Before work

- Read `docs/standards.md`, `docs/engineering-notes.md`, and the guide closest to the changed area. For root or cross-repository work, assign owners with `docs/PROJECT.md` first.
- Before membership, gitlink, or pin changes, inspect live declarations and run `bun run report:baseline`. Afterward compare `git submodule status` and gitlinks.
- For shared UI, read the provider and consumer contracts in `all-web-ui`, `keelim-vercel`, and `rich/web`; use `bun run report:shared-ui` to scope verification.
- Before runtime, authentication, or knowledge-input work, read `docs/security.md` and `docs/operations.md`, then confirm the owner and destination. Python and Bun changes must not expand one another's membership implicitly.
- Use the owning codebase-memory index for structure, text search for configuration/prose/literals or coverage gaps. For ideas, begin at `docs/CODEMAPS/README.md` and read only relevant maps.

## Problem routing

Stop the affected action and immediately report lost work, unauthorized child changes, exposed secrets, writes to an unconfirmed database, or concurrent PGLite access that could corrupt the store. Record other unresolved issues, reproduction conditions, impact, and the reason they remain unresolved in `docs/tracking/findings.md`. Fix in-scope defects that can be resolved now and report the actual check results.
