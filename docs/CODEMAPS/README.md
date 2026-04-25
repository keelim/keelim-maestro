# keelim-maestro — Codemaps

> Last updated: 2026-05-03

This directory documents the architecture and structure of the **keelim-maestro** workspace superproject.

## Index

| File | Contents |
|------|----------|
| [WORKSPACE.md](WORKSPACE.md) | Workspace topology, child repositories, policies |
| [SUBMODULES.md](SUBMODULES.md) | Registered Git submodules — remotes, branches, purpose |
| [SCRIPTS.md](SCRIPTS.md) | Root-level helper scripts — behaviour, flags, exit codes |
| [keelim-maestro.md](keelim-maestro.md) | Reviewed root and workspace-management codemap for this coordination repo |
| [projects/README.md](projects/README.md) | Maestro-managed generated codemaps for available child repositories |
| [architecture.md](architecture.md) | System topology and service boundaries |
| [backend.md](backend.md) | API routes and middleware chains |
| [data.md](data.md) | Data stores and migrations |
| [frontend.md](frontend.md) | UI surfaces and component hierarchy |
| [dependencies.md](dependencies.md) | External services and libraries |

## Design

| File | Contents |
|------|----------|
| [../design/design-system.md](../design/design-system.md) | Keelim Design System — tokens, themes, components, and maintenance rules |

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
│   └── CODEMAPS/        ← root maps plus managed child-project snapshots
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
- `keelim-vercel` — web / Vercel deployment project (`main`)
- `toto` — local KBO Streamlit dashboard (`main`)

Autonomous child repos (not registered submodules):

- `all-web-ui` — shared web UI (remote-backed, pending submodule conversion)
- `rich` — autonomous; currently ahead of origin, pending reconciliation
- `quant` — intentionally excluded when present; absent in this checkout

Managed child codemap snapshots live under [`projects/`](projects/). They are
generated from child sources and stored here so `maestro` can manage the whole
workspace from the root without flattening child Git ownership.
