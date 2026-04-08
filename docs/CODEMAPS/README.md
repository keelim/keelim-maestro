# keelim-maestro — Codemaps

This directory documents the architecture and structure of the **keelim-maestro** workspace superproject.

## Index

| File | Contents |
|------|----------|
| [WORKSPACE.md](WORKSPACE.md) | Workspace topology, child repositories, policies |
| [SUBMODULES.md](SUBMODULES.md) | Registered Git submodules — remotes, branches, purpose |
| [SCRIPTS.md](SCRIPTS.md) | Root-level helper scripts — behaviour, flags, exit codes |

## Quick orientation

`keelim-maestro` is a **Git superproject / workspace coordination layer**.
It does _not_ vendor child-repository source code; it tracks their remote-backed
commit pointers via `.gitmodules` and supplies shared documentation and helper
scripts.

```
keelim-maestro/
├── .gitmodules          ← submodule declarations
├── AGENTS.md            ← AI-agent operating guidance
├── README.md            ← human-facing workspace overview
├── docs/
│   └── CODEMAPS/        ← this directory
└── scripts/
    ├── update-subrepos.sh
    ├── verify-all-web-ui-integration.sh
    └── verify-keelim-plugin-rename.sh
```

Registered submodules (pinned via `.gitmodules`):

- `all` — main Android Gradle project (`develop`)
- `android-support` — GitHub Action for Android build workflows (`main`)
- `c2g-proxy` — Claude Code ↔ LiteLLM ↔ Gemini bridge (`main`)
- `Keelim-Knowledge-Vault` — documentation knowledge base (`main`)
- `keelim-plugin` — plugin project (`main`)
- `keelim-vercel` — web / Vercel deployment project (`develop`)

Autonomous child repos (not registered submodules):

- `all-web-ui` — shared web UI (remote-backed, pending submodule conversion)
- `rich` — autonomous; 30 commits ahead of origin, pending reconciliation
- `quant` — intentionally excluded; no remote
