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

### Module layout
```
all/
├── app-arducon/          # DeepLink tester, QR scanner, JSON formatter, device info
├── app-cnubus/           # CNU bus real-time info, Google Maps integration
├── app-comssa/           # Financial calculators, economic calendar, flashcards
├── app-my-grade/         # Grade calculator, timer, study analytics, vocabulary
├── app-nanda/            # NANDA diagnosis, food/exercise tracker, water intake
├── app-mysenior/         # Minimal app for seniors
├── core/                 # Shared modules: common, data, database, network, UI, etc.
├── feature/              # Feature modules: settings, UI screens, web
├── shared/               # Kotlin Multiplatform (KMP) shared code
├── build-logic/          # Custom Gradle convention plugins
├── benchmarks/           # Performance benchmarking
├── widget/               # Android widgets
├── allIos/               # iOS Xcode project
└── all-rust-lib/         # Rust library (Cargo project)
```

### Architecture pattern
Clean Architecture + MVVM + Unidirectional Data Flow (UDF):
- **Presentation**: Jetpack Compose screens in `app-*/` and `feature/ui-*/`
- **Domain**: Use cases in `core:domain`
- **Data**: Repository implementations in `core:data`, interfaces in `core:data-api`
- **Storage**: Room DB in `core:database`, Retrofit in `core:network`

---

## `android-support` — GitHub Action for Android Workflows

| Field | Value |
|-------|-------|
| Path | `android-support/` |
| Remote | https://github.com/keelim/android-support |
| Tracked branch | `main` |
| Language / toolchain | TypeScript / Node.js |
| Purpose | GitHub Action providing Android build workflow support (signing, release uploads, Play Store "What's New") |

### Key files inside the submodule
```
android-support/
├── action.yml            # GitHub Action interface definition
├── package.json          # NPM dependencies
├── tsconfig.json         # TypeScript configuration
├── src/
│   ├── index.ts          # Entry point
│   ├── main.ts           # Action main logic
│   ├── edits.ts          # Edit/release operations
│   ├── signing.ts        # APK/AAB signing support
│   ├── whatsnew.ts       # Play Store "What's New" text handling
│   ├── input-validation.ts
│   └── utils/            # Logger, IO utilities
└── __tests__/            # Jest test suite
```

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
| Language / toolchain | Markdown / Obsidian |
| Purpose | Shared knowledge base and documentation for the workspace |

### Content categories
- `AI/`, `Android/`, `Books/`, `Code/`, `Computer Science/`
- `KMP/`, `Language/`, `System Design/`, `HTTP/`
- `convention/`, `service/`, `test/`

---

## `keelim-plugin` — Plugin Project

| Field | Value |
|-------|-------|
| Path | `keelim-plugin/` |
| Remote | https://github.com/keelim/keelim-plugin.git |
| Tracked branch | `main` |
| Previous name | `keelim-skill` (renamed; continuity preserved via `.gitmodules` and submodule metadata) |
| Purpose | Plugin / skill definitions for AI-assisted workflows |

### Skills
```
keelim-plugin/skills/
├── release-automation/   # Date-based Android release workflow
├── tech-post-maker/      # Technical post writing skill
└── ralplan-team/         # Team planning skill
```

Each skill has a `SKILL.md` definition and optional `agents/openai.yaml` metadata.

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
