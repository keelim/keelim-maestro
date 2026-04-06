# Registered Submodules

All entries below are declared in `/.gitmodules` and are pinned to a specific
commit when the root superproject is cloned with `git submodule update --init --recursive`.

---

## `all` — Main Android Project

| Field | Value |
|-------|-------|
| Path | `all/` |
| Remote | https://github.com/keelim/all.git |
| Tracked branch | `develop` |
| Language / toolchain | Kotlin / Android Gradle |
| Expected architecture | Clean Architecture, Jetpack Compose, multi-module |

### Key dependencies (inferred)
- Jetpack Compose (UI)
- Hilt (dependency injection)
- Room (local database)
- Retrofit (HTTP)
- Kotlin Coroutines / Flow

### Expected module layout
```
all/
├── app/                  # Application module
├── core/                 # Shared core utilities
├── data/                 # Data layer (repositories, DAOs, API services)
├── domain/               # Domain layer (use-cases, models, interfaces)
└── feature/              # Feature modules (one per screen/flow)
```

---

## `android-support` — Android Support Libraries

| Field | Value |
|-------|-------|
| Path | `android-support/` |
| Remote | https://github.com/keelim/android-support |
| Tracked branch | `main` |
| Language / toolchain | Kotlin / Android Gradle |
| Purpose | Shared Android utilities consumed by `all` and other Android projects |

---

## `c2g-proxy` — Claude Code ↔ LiteLLM ↔ Gemini Bridge

| Field | Value |
|-------|-------|
| Path | `c2g-proxy/` |
| Remote | https://github.com/keelim/c2g-proxy.git |
| Tracked branch | `main` |
| Language / toolchain | Python, managed with `uv` |
| Purpose | Translation layer enabling Claude Code CLI to use LiteLLM / Gemini as the backend provider |

### Key files inside the submodule
```
c2g-proxy/
├── .env.example                                  # Config template — copy to .env before running
├── README.md
├── docs/
│   ├── claude-code-via-litellm-gemini.md         # Setup guide
│   └── claude-code-via-litellm-gemini-verification.md
└── scripts/litellm/                              # Bridge start / verify helpers
```

### Bootstrap
```bash
cd c2g-proxy
cp .env.example .env          # fill in API keys
uv sync
# then run the start script in scripts/litellm/
```

---

## `Keelim-Knowledge-Vault` — Documentation Knowledge Base

| Field | Value |
|-------|-------|
| Path | `Keelim-Knowledge-Vault/` |
| Remote | https://github.com/keelim/Keelim-Knowledge-Vault.git |
| Tracked branch | `main` |
| Language / toolchain | Markdown / documentation |
| Purpose | Shared knowledge base and documentation for the workspace |

---

## `keelim-plugin` — Plugin Project

| Field | Value |
|-------|-------|
| Path | `keelim-plugin/` |
| Remote | https://github.com/keelim/keelim-plugin.git |
| Tracked branch | `main` |
| Previous name | `keelim-skill` (renamed; continuity preserved via `.gitmodules` and submodule metadata) |
| Purpose | Plugin / IDE integration or extensibility framework |

### Rename history
The submodule directory was renamed from `keelim-skill` to `keelim-plugin`.
The rename is verified by `scripts/verify-keelim-plugin-rename.sh`.

---

## `keelim-vercel` — Web / Vercel Deployment Project

| Field | Value |
|-------|-------|
| Path | `keelim-vercel/` |
| Remote | https://github.com/keelim/keelim-vercel.git |
| Tracked branch | `develop` |
| Language / toolchain | Node.js / JavaScript (Vercel deployment) |
| Purpose | Web frontend and deployment automation via Vercel |

---

## Autonomous Repos (not registered submodules)

These repositories exist under the workspace root and are surfaced by helper
scripts, but are **not** declared in `.gitmodules`.

### `all-web-ui`
- Remote: https://github.com/keelim/all-web-ui.git
- Branch: `main`
- Status: Remote-backed; submodule conversion deferred pending workspace cleanup
- Policy: Include in status helpers; do not add as local-path submodule

### `rich`
- Remote: https://github.com/keelim/rich.git
- Branch: `master`
- Status: ~30 local commits ahead of `origin/master`; needs reconciliation before pinning

### `quant`
- Remote: **none**
- Status: Dirty local-only repository
- Policy: Do **not** create a remote; do **not** add as submodule; keep autonomous
