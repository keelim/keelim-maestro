# Workspace Architecture

## Overview

`keelim-maestro` is a **federated multi-repository workspace** (Git superproject).
Each child directory is its own autonomous Git repository with its own history,
branch model, and build toolchain. The root repository's sole responsibility is
workspace-level coordination: submodule pointers, documentation, and helper scripts.

## Topology

```mermaid
flowchart TB
    root["keelim-maestro\n(superproject)"]

    root --> coord["Coordination files\nAGENTS.md / README.md\n.gitignore / .gitmodules"]
    root --> docs["docs/CODEMAPS/\narchitecture documentation"]
    root --> idea["idea/\nproject idea tracking"]
    root --> scripts["scripts/\nhelper scripts"]
    root --> submodules["Registered submodules\n(pinned via .gitmodules)"]
    root --> autonomous["Autonomous child repos\n(tracked in scripts only)"]

    submodules --> all["all\nAndroid · develop"]
    submodules --> android["android-support\nGitHub Action · main"]
    submodules --> vault["Keelim-Knowledge-Vault\nDocumentation · main"]
    submodules --> plugin["keelim-plugin\nPlugin · main"]
    submodules --> vercel["keelim-vercel\nWeb/Vercel · main"]
    submodules --> toto["toto\nKBO dashboard · main"]

    autonomous --> webui["all-web-ui\nWeb UI · main (remote-backed)"]
    autonomous --> rich["rich\nWeb/Node.js · master (ahead of origin)"]
    autonomous --> quant["quant\n(local-only, no remote)"]
    autonomous --> console["agent-skill-console\nTauri desktop · local-only"]
```

## Child Repository Catalogue

| Path | Remote | Default branch | Type | Registration |
|------|--------|----------------|------|--------------|
| `all` | https://github.com/keelim/all | `develop` | Android (Gradle multi-module) | Registered submodule |
| `all-web-ui` | https://github.com/keelim/all-web-ui | `main` | Shared web UI | Autonomous (pending submodule) |
| `android-support` | https://github.com/keelim/android-support | `main` | TypeScript / Node.js GitHub Action | Registered submodule |
| `Keelim-Knowledge-Vault` | https://github.com/keelim/Keelim-Knowledge-Vault | `main` | Documentation | Registered submodule |
| `keelim-plugin` | https://github.com/keelim/keelim-plugin | `main` | Plugin project | Registered submodule |
| `keelim-vercel` | https://github.com/keelim/keelim-vercel | `main` | Web / Vercel deployment | Registered submodule |
| `toto` | https://github.com/keelim/toto | `main` | Local KBO Streamlit dashboard | Registered submodule |
| `agent-skill-console` | none | n/a | Tauri desktop app (skill/agent inventory) | Local-only, intentionally excluded |
| `quant` | none | n/a | local-only (no remote) | Intentionally excluded |
| `rich` | https://github.com/keelim/rich | `master` | Web / Node.js | Autonomous (pending reconciliation) |

## Architectural Principles

### 1. Child-repository autonomy
Each child directory is its own Git context. When modifying code inside a child
repo, enter that directory and follow its own `AGENTS.md` if present. Root-level
commits must not edit child-repo source files.

### 2. Remote-backed submodules only
Submodules are added via their GitHub remote URL only. Local-path submodules are
prohibited because they break reproducible clone workflows.

### 3. Smallest reversible root diff
Root changes should prefer updating documentation, `.gitmodules` pointers, or
helper scripts rather than automating child-repo operations. Automation is
introduced only after child repos are in a clean, pinnable state.

### 4. Submodule expansion gate
Expanding `.gitmodules` to cover additional child repos is blocked until:
- All existing child repos are clean (no dirty working trees)
- `rich` local commits ahead of origin are reconciled / pushed
- `quant` dirty state is explicitly resolved or preserved
- Any other diverged repos are normalised

## Bootstrap

```bash
git clone https://github.com/keelim/keelim-maestro.git
cd keelim-maestro
git submodule update --init --recursive
```

## Verification Commands

```bash
# Root status (ignores submodule internals)
git status --short

# Root status (includes submodule dirty/new states)
git status --ignore-submodules=none

# Submodule commit pointers
git submodule status

# Branch / dirty state inside each submodule
git submodule foreach git status --short --branch

# Confirm submodule gitlinks
git ls-files --stage | grep 160000
```

## Safe Scope for Root Commits

Files that are safe to modify at the root level:

- `AGENTS.md`
- `README.md`
- `.gitignore`
- `.gitmodules`
- `docs/` (including this directory)
- `idea/`
- `scripts/`

Files and directories that must **not** be edited from the root:
- Any source file inside a child-repo directory (`all/`, `android-support/`, etc.)

## Current Submodule Snapshot

> Last updated: 2026-05-05

| Path | Pinned commit | Branch | Status |
|------|---------------|--------|--------|
| `all` | `edac30d2` | `develop` | Checked out |
| `android-support` | `485a2e40` | `main` | Checked out |
| `Keelim-Knowledge-Vault` | `e7409730` | `main` | Checked out |
| `keelim-plugin` | `3e41d105` | `main` | Checked out |
| `keelim-vercel` | `5aa9c8bb` | `develop` | Checked out |
| `toto` | `a942e6b` | `main` | Checked out |
| `all-web-ui` | — | `main` | Autonomous (not in .gitmodules) |
| `rich` | — | `master` | Autonomous, commits ahead of origin |
| `quant` | — | — | Local-only (no remote) |
