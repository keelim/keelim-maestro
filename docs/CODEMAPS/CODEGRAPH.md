# CodeGraph Operating Contract

> Last updated: 2026-05-24

This workspace can use CodeGraph at two levels, but the levels have different
jobs. The default operating model is a root dispatcher that routes to
child-repo graphs. A child-repo graph is the implementation graph.

## Role Split

| Graph | Use for | Do not use for |
|------|---------|----------------|
| Root dispatcher | Selecting the relevant child repo, shared docs/scripts, contract checks, status sweeps | Indexing child source into one aggregate root graph |
| Root `.codegraph/` | Optional coordination-only root-owned docs/scripts/shared config, only if child-repo noise is controlled | Implementation edits inside child repos, broad symbol indexing of child source trees |
| Child `.codegraph/` | Actual code implementation, symbol/context/callers/callees, impact analysis, test-scope selection | Root policy changes or sibling-repo edits unless explicitly needed |

The root is a coordination layer for autonomous child repositories, not a
single vendored monorepo. Root CodeGraph must stay coordination-only unless a
future explicit policy change makes this repository a true monorepo.

## Dispatcher Helper

Use `scripts/codegraph.sh` from the workspace root to dispatch CodeGraph to
child repos without creating a root aggregate graph:

```bash
bun run cg -- list
bun run cg:status
bun run cg -- files rich --max-depth 2
bun run cg -- context keelim-plugin "skill inventory"
bun run cg -- query all-web-ui Button
bun run cg:root-check
```

The helper resolves the CodeGraph CLI from `CODEGRAPH_BIN`, then `PATH`, then
the known local CodeGraph 0.9.3 binary. It targets only active AGENTS-listed
child repos: `all`, `all-web-ui`, `android-support`, `Keelim-Knowledge-Vault`,
`keelim-plugin`, `keelim-vercel`, and `rich`.

`root`, `quant`, archived `toto`, `tools`, and `tools/crawler` are excluded dispatcher targets.
The helper never runs `codegraph init -i`; missing child graphs are reported so
they can be initialized explicitly inside the intended child repo.

## Prompt Contract

Variables:

- `{ROOT_PATH}`: absolute path to the top-level workspace
- `{SUBPROJECT_PATH}`: absolute path to the child project being changed
- `{TASK}`: current work objective
- `{BOUNDARY}`: allowed root and child edit scope
- `{VERIFY}`: expected verification command or acceptance criterion

Default prompt:

```text
The workspace root is {ROOT_PATH}, and the actual implementation target is
{SUBPROJECT_PATH}.

Goal:
{TASK}

Boundary:
{BOUNDARY}
- Use the root for workspace maps, shared documents, shared scripts, and shared contract checks.
- Treat the subproject as the default unit for real code changes and test verification.
- Read sibling subprojects only when explicitly needed, and report the reason before editing them.

CodeGraph use:
- First check whether `.codegraph/` exists in both the root and the subproject.
- If the root `.codegraph/` exists, use it only to understand root structure, shared contracts, and cross-project links.
- If the subproject `.codegraph/` exists, use it for implementation-related symbol/context/callers/callees/impact exploration.
- If `.codegraph/` is missing, do not initialize it immediately. Report whether `codegraph init -i` is needed and whether `.gitignore` already excludes the right targets.
- Use `rg` and direct file reads as backup only when CodeGraph results are missing or insufficient.

Workflow:
1. Inspect workspace structure and relevant shared contracts from the root.
2. Inspect the real entry points and impact range from the subproject.
3. Briefly state which files will change and why.
4. Implement only within the approved boundary.
5. Run {VERIFY} or the narrowest repo-native verification.
6. Report root impact, subproject changes, verification results, and remaining risks separately.
```

## Root Setup Checklist

Use this when checking whether `{ROOT_PATH}` is safe to initialize as a
CodeGraph root:

```text
Check whether {ROOT_PATH} is safe to use as a CodeGraph root.

Check:
- Whether `.codegraph/` exists.
- Whether the root `.gitignore` properly excludes child repos, `node_modules`, `dist`, `build`, `.env`, and generated output.
- Whether the root is a true monorepo or a coordination layer for independent child repos.
- Whether the root CodeGraph should index docs/scripts/shared config or full child source trees.

Return one of these conclusions:
1. Root CodeGraph initialization recommended: the root has real exploration value and child-repo noise is controlled.
2. Root CodeGraph deferred: full child repos would be mixed into the index and create too much noise.
3. Root gitignore cleanup recommended before initialization: exclusion coverage needs to be fixed first.

If initialization is appropriate, only present this execution plan:
codegraph init -i
codegraph status
codegraph files . --max-depth 2
```

Do not initialize CodeGraph as part of planning-only work. Initialization is an
implementation step and should be called out before it runs.

## Operating Rules

- Start at the root for architecture, common contracts, and deciding which
  project is relevant.
- Start in the child repo for implementation, bug fixes, impact analysis, and
  test-scope selection.
- If both graphs exist, use the root graph as coordination context and the
  child graph as implementation context.
- If `.codegraph/` is missing, report the missing graph and the current ignore
  coverage before proposing `codegraph init -i`.
- Use `rg` and direct file reads only when CodeGraph is missing or insufficient.
- Keep `.codegraph/` uncommitted; it is generated local index state.
- Treat sibling repos as read-only context unless the requested change explicitly
  crosses that boundary.

## Verification Matrix

| Situation | Minimum evidence |
|-----------|------------------|
| Root CodeGraph setup check | `codegraph status`, `codegraph files . --max-depth 2`, and a root `.gitignore` exclusion check |
| Child CodeGraph setup check | `codegraph status` from the child repo and relevant context/impact/affected output |
| Implementation change | Narrowest child repo test/lint/build command that matches the touched code |
| Cross-project change | Root contract evidence plus each touched child repo's native verification |
| Planning-only update | File inspection, `git diff --check`, and a clear note that no `.codegraph/` initialization ran |

## Current Root Assessment

As of 2026-05-24, root CodeGraph initialization is deferred:

- Root-owned CodeGraph value exists for `AGENTS.md`, `README.md`,
  `docs/CODEMAPS/`, `docs/idea/`, root `package.json` / `pyproject.toml`, and
  helper scripts.
- A root `codegraph init -i /Users/keelim/Desktop/keelim-maestro` run indexed
  child source trees such as `all`, `android-support`, and `keelim-vercel`, so
  the root graph was removed and child graphs were kept.
- Child source trees should not be part of the root index by default.
- Root `.gitignore` excludes `.codegraph/`, dependency folders, common generated
  output, environment files, and known child-repo working trees for tools that
  honor `.gitignore`.
- Use `scripts/codegraph.sh` as the root-to-child dispatcher unless a future
  CodeGraph release provides a reliable root-owned-file-only index mode.
