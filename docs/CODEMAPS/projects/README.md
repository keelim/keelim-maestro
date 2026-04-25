# Managed Project Codemaps

> Last updated: 2026-04-25

`keelim-maestro` centrally keeps these source-led snapshots for child projects.
The files in this directory are generated from each child repository's live
source tree, but they are stored here so the maestro workspace can manage
cross-repo orientation without pretending child source is root-owned.

## Generated Snapshots

| Project | Codemap | Files scanned | Shape |
| --- | --- | ---: | --- |
| `all` | [all.md](all.md) | 1,013 | Java/Kotlin/Gradle |
| `all-web-ui` | [all-web-ui.md](all-web-ui.md) | 46 | Node/JavaScript |
| `android-support` | [android-support.md](android-support.md) | 36 | Node/JavaScript |
| `Keelim-Knowledge-Vault` | [Keelim-Knowledge-Vault.md](Keelim-Knowledge-Vault.md) | 218 | Markdown / source repository |
| `keelim-plugin` | [keelim-plugin.md](keelim-plugin.md) | 11 | Skill/plugin source repository |
| `keelim-vercel` | [keelim-vercel.md](keelim-vercel.md) | 587 | Node/JavaScript |
| `rich` | [rich.md](rich.md) | 1,621 | Node/JavaScript, Python, Docker |
| `toto` | [toto.md](toto.md) | 28 | Node/JavaScript, Python |

## Not Collected In This Checkout

| Project | Reason |
| --- | --- |
| `quant` | Directory absent in this checkout; root policy still treats it as excluded/autonomous when present. |

## Refresh Command

From the workspace root, run the generator once per available child repo:

```bash
python3 keelim-plugin/skills/codebase-codemap/scripts/generate_codemap.py <child-path> --output-dir docs/CODEMAPS/projects
```

Use [../keelim-maestro.md](../keelim-maestro.md) for root-level ownership,
submodule state, and cross-repo verification commands before acting on these
project snapshots.
