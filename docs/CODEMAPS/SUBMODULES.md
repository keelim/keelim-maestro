# Submodules Codemap

<!-- Generated: 2026-09-05 -->
Last updated: 2026-09-05

## Registered Submodules

Sourced from `.gitmodules` and `git ls-files --stage | grep 160000`.

| Submodule path | Remote URL | Default branch | Pinned commit |
| --- | --- | --- | --- |
| `all` | https://github.com/keelim/all.git | `develop` | `dbd6ce9e06fb914e6f0e1170b27efb10bb05da68` |
| `Keelim-Knowledge-Vault` | https://github.com/keelim/Keelim-Knowledge-Vault.git | `main` | `2cfffa10aaa7e5568bfeb7305e26c6cea48cbcba` |
| `keelim-plugin` | https://github.com/keelim/keelim-plugin.git | `main` | `0e05ea44da5cca600f731802fbd879b31a7367d7` |
| `keelim-vercel` | https://github.com/keelim/keelim-vercel.git | `develop` | `c0e876927156ec66deb8d9b7d6d19e3d8db48d4a` |

## Autonomous Local Repos (not in .gitmodules)

| Path | Remote | Branch | Notes |
| --- | --- | --- | --- |
| `all-web-ui` | github.com/keelim/all-web-ui | main | Public remote; pending submodule conversion |
| `rich` | github.com/keelim/rich | master | Dirty working tree; commits ahead of origin; freeze/split before pinning |
| `youtube` | github.com/keelim/youtube | — | YouTube automation; active Bun + uv workspace member |
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
