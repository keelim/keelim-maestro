# `keelim-plugin` Codemap

<!-- Generated: 2026-06-25 -->

**Type:** Registered Git submodule
**Remote:** https://github.com/keelim/keelim-plugin.git
**Branch:** main
**Pinned commit:** `a3463396c95dcd4749727bf1f32495db45bba220`

## Shape

Python skills and automation plugin for Claude / Codex agents.

## Key Contents

- `skills/codebase-codemap/scripts/generate_codemap.py` — codemap generator invoked by root `scripts/refresh-codemaps.py`
- Agent skill definitions for codebase analysis and coordination

## Notes

- This submodule must be initialized for `scripts/refresh-codemaps.py` to run.
- Run `git submodule update --init keelim-plugin` to hydrate.
- Full codemap requires child hydration. Re-run `scripts/refresh-codemaps.py` after initializing.
