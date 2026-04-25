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
| Pinned commit | `778491a6c` |
| Language / toolchain | Kotlin / Android Gradle (Kotlin DSL) |
| Architecture | Clean Architecture + MVVM + Unidirectional Data Flow (UDF) |

### Build configuration
| Setting | Value |
|---------|-------|
| Min SDK | 26 (Android 8.0+) |
| Target SDK | 36 (Android 16) |
| JVM target | 17 |
| Kotlin | 1.9+ |
| Core library desugaring | enabled |

### Key dependencies
- **UI**: Jetpack Compose, Material 3
- **DI**: Hilt
- **Storage**: Room (SQLite), DataStore Proto
- **Network**: Retrofit + OkHttp
- **Async**: Kotlin Coroutines + Flow
- **Multiplatform**: Kotlin Multiplatform (KMP)
- **Push**: Firebase Cloud Messaging (FCM)

### App modules (6 Android applications)
| Module | Files | Description |
|--------|-------|-------------|
| `app-my-grade` | 237 | Grade calculator, study timer, analytics, vocabulary learning |
| `app-arducon` | 210 | DeepLink tester, QR scanner, JSON formatter, device info |
| `app-nanda` | 206 | NANDA diagnosis, food/exercise tracker, water intake monitor |
| `app-comssa` | 28 | Financial calculators, economic calendar, flashcards |
| `app-cnubus` | 12 | CNU bus real-time info, Google Maps integration |
| `app-mysenior` | 4 | Minimal accessibility-friendly app for seniors |

### Core modules (14 shared modules)
| Module | Files | Description |
|--------|-------|-------------|
| `core:component` | 144 | Shared Compose UI, custom Material 3 components, theme utilities |
| `core:data` | 85 | Repository implementations, data sources, FCM service |
| `core:common-android` | 61 | Android-specific utilities, extensions, helpers |
| `core:model` | 38 | Shared domain data models |
| `core:database` | 35 | Room DB schema, entities, DAOs, mappers |
| `core:data-api` | 25 | Repository interfaces / API contracts (boundary layer) |
| `core:common` | 24 | Pure Kotlin utilities (no Android dependencies) |
| `core:network` | 18 | Retrofit, OkHttp, HTTP interceptors |
| `core:resource` | 9 | Shared string/drawable resources |
| `core:designsystem` | 5 | Material 3 design tokens, color/typography system |
| `core:domain` | 4 | Use cases |
| `core:navigation` | 2 | Navigation graphs, route models |
| `core:testing` | 2 | Test utilities and helpers |
| `core:datastore-proto` | — | Protocol Buffer DataStore definitions |

### Feature modules
| Module | Files | Description |
|--------|-------|-------------|
| `feature:ui-setting` | 104 | Settings screens, animated theme selector, preferences UI |
| `feature:ui-scheme` | 14 | Scheme-related UI |
| `feature:ui-web` | 4 | WebView screens |
| `feature:settings-*` | — | Modular settings: theme, notification, alarm, device, admin, lab |
| `feature:app-function` | — | Shared app-level feature screens |

### Other modules
```
all/
├── shared/               # Kotlin Multiplatform shared code, DB models/DAOs
├── build-logic/          # 17 custom Gradle convention plugins
├── benchmarks/           # Performance benchmarking
├── widget/               # Android widget implementations
├── composeApp/           # Compose Multiplatform app shell
├── catalog/              # Version catalog definitions
├── allIos/               # iOS Xcode project
└── all-rust-lib/         # Rust library (Cargo project)
```

### Architecture layers
- **Presentation**: Jetpack Compose screens in `app-*/` and `feature/ui-*/`; ViewModels expose `StateFlow`
- **Domain**: Use cases in `core:domain`
- **Data**: Repository implementations in `core:data`, interfaces in `core:data-api`
- **Storage**: Room DB in `core:database`, Retrofit in `core:network`

### Coding conventions
- UI text must specify `style` and `color` explicitly (no defaults)
- Dates/numbers use shared formatters (ISO/epoch for storage, locale-aware for display)
- All apps use Hilt for DI; LiveData is not used — `StateFlow`/`Flow` only
- No global mutable state; no string concatenation in SQL
- Coroutines must not block the main thread

### CI/CD workflows
| Workflow | Trigger |
|----------|---------|
| `ci.yml` | Main CI — build + test on every PR |
| `app_my_grade.yml` | Per-app build for `app-my-grade` |
| `app_arducon.yml` | Per-app build for `app-arducon` |
| `app_nanda.yml` | Per-app build for `app-nanda` |
| `app_comssa.yml` | Per-app build for `app-comssa` |
| `app_cnubus.yml` | Per-app build for `app-cnubus` |
| `app_deploy.yml` | Shared release deployment |
| `release.yml` | Release workflow |
| `release_tag.yml` | Tag-triggered release |
| `gh_page.yml` | GitHub Pages publication |
| `slack.yml` | Slack notifications |

---

## `android-support` — GitHub Action for Android Workflows

| Field | Value |
|-------|-------|
| Path | `android-support/` |
| Remote | https://github.com/keelim/android-support |
| Tracked branch | `main` |
| Pinned commit | `485a2e40` (v0.0.8-4) |
| Language / toolchain | TypeScript / Node.js (Bun package manager) |
| Purpose | GitHub Action for APK/AAB signing and Google Play Console upload |

### Key files inside the submodule
```
android-support/
├── action.yml            # GitHub Action interface definition
├── package.json          # dependencies (uses Bun)
├── tsconfig.json         # TypeScript configuration (ES2018, CommonJS)
├── src/
│   ├── main.ts           # Action entry point
│   ├── edits.ts          # Google Play Edit workflow
│   ├── signing.ts        # APK/AAB signing
│   ├── whatsnew.ts       # Play Store "What's New" text handling
│   ├── input-validation.ts
│   └── utils/            # Logger, IO utilities
├── __tests__/            # Jest (ts-jest) test suite
└── lib/index.js          # compiled output (@vercel/ncc)
```

### Action inputs / outputs
- **Inputs**: `type` (sign/upload), `serviceAccount`, `packageName`, `releaseFiles`, `track`, `status`, `userFraction`
- **Outputs**: `signedReleaseFile(s)`, `internalSharingDownloadUrl`, `nofSignedReleaseFiles`

### Build commands
```bash
bun install
bun run build   # generates lib/index.js
bun run jest    # run tests
```

---

## `Keelim-Knowledge-Vault` — Documentation Knowledge Base

| Field | Value |
|-------|-------|
| Path | `Keelim-Knowledge-Vault/` |
| Remote | https://github.com/keelim/Keelim-Knowledge-Vault.git |
| Tracked branch | `main` |
| Pinned commit | `d82b20d3` |
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
| Pinned commit | `156059ac` |
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
| Tracked branch | `main` |
| Pinned commit | `e91f0eec` |
| Language / toolchain | Node.js / JavaScript (Vercel deployment) |
| Purpose | Web frontend deployed on Vercel; integrates `all-web-ui` component library |

---

---

## `toto` — KBO Baseball Dashboard

| Field | Value |
|-------|-------|
| Path | `toto/` |
| Remote | https://github.com/keelim/toto.git |
| Tracked branch | `main` |
| Pinned commit | — (no gitlink committed to index yet) |
| Language / toolchain | Python / Streamlit |
| Purpose | Read-only KBO win/loss dashboard; reproducible season-data pipeline |

### Status

Declared in `.gitmodules` but the gitlink has **not** been committed to the git index.
The directory is absent on a fresh clone until the pending gitlink is committed.

To hydrate for local development, clone manually:

```bash
git clone https://github.com/keelim/toto.git toto
```

### Bun workspace integration

`toto` is included in the root Bun workspace (`package.json`) as workspace path `toto`.
The package name reported is `toto-kbo-streamlit-dashboard`. Root-level scripts:

| Script | Command |
|--------|---------|
| `bun run dev:toto` | Start Streamlit dev server |
| `bun run test:toto` | Run test suite |
| `bun run verify:toto` | Run reproducibility verification |

### Architecture notes

- **Frontend**: Streamlit app (`streamlit_app/Home.py`); read-only, no write paths
- **Data pipeline**: `bun run bootstrap` → `bun run seed` → populate local fixtures
- **Provider pattern**: thin `provider` interface separating game-result / standings data from the UI (CSV, fixture, or API backed)
- **Smoke gate**: `bun run verify` validates boot, home import, and read-only contract

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
- Type: Web / Node.js (contains `rich/web/` Next.js app that imports `all-web-ui`)
- Status: Local commits ahead of `origin/master`; needs reconciliation before pinning

### `quant`
- Remote: **none**
- Status: Dirty local-only repository
- Policy: Do **not** create a remote; do **not** add as submodule; keep autonomous
