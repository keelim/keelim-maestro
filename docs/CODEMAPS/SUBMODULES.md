# Submodules Codemap

<!-- Generated: 2026-06-23 -->
Last updated: 2026-06-23

## Registered Submodules

Sourced from `.gitmodules` and `git ls-files --stage | grep 160000`.

| Submodule path | Remote URL | Default branch | Pinned commit |
| --- | --- | --- | --- |
| `all` | https://github.com/keelim/all.git | `develop` | `0643bab4281700c08c12492af7fe0d0a0663d12e` |
| `android-support` | https://github.com/keelim/android-support | `main` | `485a2e404248182f48b01266c2d2ab8eb67145aa` (v0.0.8-4) |
| `Keelim-Knowledge-Vault` | https://github.com/keelim/Keelim-Knowledge-Vault.git | `main` | `15b29c11b7199d6f2c97a518781de97bbbea0dfd` |
| `keelim-plugin` | https://github.com/keelim/keelim-plugin.git | `main` | `a3463396c95dcd4749727bf1f32495db45bba220` |
| `keelim-vercel` | https://github.com/keelim/keelim-vercel.git | `develop` | `1304f1216351f268636c09e43a3315071ed6c769` |
| `toto` | https://github.com/keelim/toto.git | `main` | `5897ef441cb13c550c83a5392097bc46423b3391` |

## Autonomous Local Repos (not in .gitmodules)

| Path | Remote | Branch | Notes |
| --- | --- | --- | --- |
| `all-web-ui` | github.com/keelim/all-web-ui | main | Public remote; clean vs origin/main; pending submodule conversion |
| `rich` | github.com/keelim/rich | master | Dirty working tree; commits ahead of origin; freeze/split before pinning |
| `quant` | none | — | Intentionally excluded; no remote |

## Bootstrap Commands

```bash
# Initialize/update all registered submodules
git submodule update --init --recursive

# Status check
git submodule status
git ls-files --stage | grep 160000

# Subrepo helper (includes autonomous repos)
./scripts/update-subrepos.sh status
./scripts/update-subrepos.sh dry-run
./scripts/update-subrepos.sh update
```

## Expansion Blockers

Before registering new submodules, resolve:
1. `rich` dirty/ahead state — freeze/split before pinning
2. `all-web-ui` — pending reconciliation of workspace blockers

When adding new submodules, always use remote-backed URLs (never local paths).
