# `Keelim-Knowledge-Vault` Codemap

<!-- Generated: 2026-06-28 -->

**Type:** Registered Git submodule
**Remote:** https://github.com/keelim/Keelim-Knowledge-Vault.git
**Branch:** main
**Pinned commit:** `15b29c11b7199d6f2c97a518781de97bbbea0dfd`

## Shape

Obsidian/Markdown knowledge vault — flat notes + structured frontmatter + PKM content.

## Key Verification Scripts

Root-owned scripts check vault health:
- `scripts/improvements/verify_knowledge_vault_automation.py` — automation compliance
- `scripts/improvements/verify_knowledge_vault_frontmatter.py` — frontmatter validity
- `scripts/improvements/verify_knowledge_vault_links.py` — internal link integrity

## GBrain Integration

The Knowledge Vault is a curated import source for the GBrain knowledge system
(`~/brain` operator repo). See [backend.md](../backend.md) for GBrain details.

## Notes

- Not initialized in a fresh root checkout. Run `git submodule update --init Keelim-Knowledge-Vault` to hydrate.
- Full codemap requires child hydration. Re-run `scripts/refresh-codemaps.py` after initializing.
