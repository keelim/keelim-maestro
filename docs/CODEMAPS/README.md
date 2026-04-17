# keelim-maestro — Codemaps

> Last updated: 2026-04-17

This directory documents the architecture and structure of the **keelim-maestro** workspace superproject.

## Index

| File | Contents |
|------|----------|
| [WORKSPACE.md](WORKSPACE.md) | Workspace topology, child repositories, policies |
| [SUBMODULES.md](SUBMODULES.md) | Registered Git submodules — remotes, branches, purpose |
| [SCRIPTS.md](SCRIPTS.md) | Root-level helper scripts — behaviour, flags, exit codes |
| [architecture.md](architecture.md) | System topology and service boundaries |
| [backend.md](backend.md) | API routes and middleware chains |
| [data.md](data.md) | Data stores and migrations |
| [frontend.md](frontend.md) | UI surfaces and component hierarchy |
| [dependencies.md](dependencies.md) | External services and libraries |

## Quick orientation

`keelim-maestro` is a **Git superproject / workspace coordination layer**.
It does _not_ vendor child-repository source code; it tracks their remote-backed
commit pointers via `.gitmodules` and supplies shared documentation and helper
scripts.

```
keelim-maestro/
├── .gitmodules          ← submodule declarations
├── AGENTS.md            ← AI-agent operating guidance
├── CLAUDE.md            ← Claude Code operating guidance (currently empty)
├── README.md            ← human-facing workspace overview
├── docs/
│   └── CODEMAPS/        ← this directory
├── idea/
│   ├── index.md         ← workspace idea index (open ideas, priorities)
│   └── <project>.md     ← per-project idea tracking (all, rich, keelim-vercel, …)
└── scripts/
    ├── update-subrepos.sh
    ├── verify-all-web-ui-integration.sh
    └── verify-keelim-plugin-rename.sh
```

Registered submodules (pinned via `.gitmodules`):

- `all` — main Android Gradle project (`develop`)
- `android-support` — GitHub Action for Android build workflows (`main`)
- `Keelim-Knowledge-Vault` — documentation knowledge base (`main`)
- `keelim-plugin` — plugin project (`main`)
- `keelim-vercel` — web / Vercel deployment project (`develop`)

> **Note:** `c2g-proxy` is declared in `.gitmodules` but its gitlink has been removed from
> the git index and the directory does not exist. It is not an active registered submodule.

Autonomous child repos (not registered submodules):

- `all-web-ui` — shared web UI (remote-backed, pending submodule conversion)
- `rich` — autonomous; 30 commits ahead of origin, pending reconciliation
- `quant` — intentionally excluded; no remote
