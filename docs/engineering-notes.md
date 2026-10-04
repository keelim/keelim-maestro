# Operational traps

## A linked document disappears from a fresh clone

Root ignore rules exclude broad documentation areas and allow selected files back in. Creating a file and linking it does not make it Git-visible. Check tracking first, then `git check-ignore -v --no-index <path>` and `git status --short --untracked-files=all -- <path>`. An ignored parent directory may need to be reopened before a file exception can work.

## A successful report still contains integration failures

Status and contract reporters can exit successfully after printing failed checks. Exit zero proves report generation. Read eligibility, skipped items, and strict-check columns, then run the relevant validator before declaring integration complete. Local ahead/behind values compare against the last fetched tracking refs, not necessarily the current remote server.

## Root cloning is not enough for installation

Package membership includes autonomous checkouts as well as submodules. Submodule initialization alone cannot prepare every Bun or uv member. Inspect missing paths and obtain each owner-approved checkout before a frozen install. Do not remove members or regenerate child lockfiles merely to get installation past an error.

Video package globs make additions and deletions affect the root lockfile. Such differences are not automatically noise.

## Pinned and executed tool versions differ

Without an activated environment, PATH can select a global binary. Compare `mise current` with actual `bun --version`, `uv --version`, and `python --version`. Report the version actually tested; do not extend that result to a pinned version that was not run.

## Local shared UI links mask independent installation failures

A workspace link does not prove registry access. Check the consumer's exact version, `@keelim` registry mapping, and public export paths. If publication or authentication is unavailable, distinguish local compatibility from standalone install readiness.

## An MCP connection does not establish method readiness

A process or health response can work while tool invocation fails. Check initialization, listing, and the intended read-only method in sequence. If an owner's index is absent, use bounded text exploration rather than another repository's index.

## Knowledge store locks and concurrent access

PGLite assumes a single active writer. Do not run `gbrain serve` alongside batch import, sync, stats, or arbitrary query CLI work. Stop the matching server, finish sequential work, and restart through its registered MCP configuration. Validate retrieval with a phrase from the original source; an input-list entry is insufficient.

## Entry guides appear to have two independent copies

Root and intro-video `CLAUDE.md` paths link to their sibling `AGENTS.md`. Replacing a link with a copy allows drift. Use `readlink` and `cmp` to confirm one source, and distinguish static parity from a new agent session reading it.
