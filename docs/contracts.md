# Workspace command contracts

Consumers are local operators and agents. Run from the root Git checkout and quote paths containing spaces. The root exposes no product HTTP API. External services authenticate separately.

## Inspection and validation

| Call and input | Output | Failure or limitation |
| --- | --- | --- |
| `bun run report:baseline` | Registration, branch, dirty state, remote, membership, eligibility table | Successful output is not approval to pin; inspect blockers and locally cached remote state |
| `./scripts/update-subrepos.sh status` | Per-repository status | No update; absent checkout or unknown remote state remains explicit |
| `./scripts/update-subrepos.sh dry-run` or `update --dry-run` | Planned fetch/fast-forward actions and skips | No fetch or source change; not proof of latest server state |
| `bun run report:shared-ui` | Provider/consumer contract and verification-readiness report | May print failed internal checks and still produce a report |
| `sh scripts/verify-all-web-ui-integration.sh [--full]` | Pass/fail for each check | Static violations fail; full mode also needs install, authentication, and build prerequisites |
| `bun run test` | Root contract checks and final result | Missing files, commands, or contract failures cause nonzero exit; does not replace child tests |

## Changeset input

`bun run changeset:validate -- <json-path>` checks the current workspace. To choose another root, use `bun scripts/validate-changeset-manifest.mjs --workspace <path> <json-path>`.

Input requires `version: 1` and a nonempty `changes` array. Each entry contains:

| Field | Meaning and validity |
| --- | --- |
| `repo` | Unique relative path to an independent Git repository inside the workspace |
| `commit` | Forty lowercase hexadecimal characters equal to that owner's current HEAD |
| `requiredChecks` | Nonempty array of existing simple check commands; no duplicates or shell operators |
| `order` | Unique positive integer; the complete set is consecutive from one |
| `rollback` | Nonempty operator-readable rollback instruction |

Unknown fields, escaping paths, dirty repositories, HEAD mismatch, and nonexistent commands are rejected. Usage errors exit 2; file, content, and repository validation failures exit 1; success exits 0. Validation never executes check commands or rollback text.

## State changes and runtime control

`./scripts/update-subrepos.sh update` fetches eligible clean repositories and uses `pull --ff-only`. Dirty repositories, unsupported branches, or repositories with local commits may be skipped. Consumers must handle both skip output and Git failures.

`scripts/repository-policy.sh` marks `rich` local-only. Status still lists it;
baseline reports `registration=local-only` and `eligibility=local-only` without
missing-remote/upstream blockers. Update and dry-run always skip it, even if a
remote is later configured. GitHub PR collection/creation and explicit URL-based
fetch/pull/push must also exclude it. Local runtime/workspace membership is
independent of this policy.

`bun run automation:local -- <action> [target]` supports inspection through `list`/`status` and validation through `verify`. Targets are `all`, `rich`, `n8n`, and `agentgateway`. `start`/`stop` require one of Rich/n8n/agentgateway. `standby` accepts those runtimes or `all`, preserving agentgateway. Results are target output and failure status; missing owner commands, cluster, or access leave the affected check failed or unverified.

`sh scripts/codex-app-server.sh [server-options]` replaces the helper with a long-running server. A missing Codex executable exits 127; an external `ws://` address without the required authentication option exits 2. Subsequent option and runtime errors belong to Codex.

## Research helpers

`node scripts/dep-freshness.mjs [--check] [--json]` returns version differences across local lockfiles as a table or JSON. `--check` reports differences without failing solely because they exist.

`node scripts/dep-audit.mjs --summary` summarizes findings, missing tools, and timeouts; its exit alone does not establish no vulnerabilities. `node scripts/security-scan.mjs [--json]` returns findings and exits 1 when findings exist. Neither replaces product-specific security verification.

Dated improvement scripts have fixed input/output paths and are not general public APIs. Inspect their date range and destinations before running. Successful generation does not mean the proposed improvements were implemented.
