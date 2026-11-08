# Setup and operation

## Prepare a new workspace

Install Git and mise first. Run from the root, after confirming the checkout and configuration are trusted:

```sh
git submodule update --init --recursive
git submodule status
mise trust
mise install
mise current
```

Prepare autonomous `all-web-ui`, `rich`, and `youtube` checkouts before package installation. Do not clone over an existing path. For a new workspace missing the shared UI repository:

```sh
git clone https://github.com/keelim/all-web-ui.git all-web-ui
```

Restore `rich` from an operator-provided local checkout or verified backup. It is
local-only under `scripts/repository-policy.sh`; do not bootstrap it from GitHub
or add a remote/upstream. Its existing Bun/Python workspace paths and local
execution, build, test, and task-management commands remain active. Exclude it
from GitHub PR collection/creation and remote synchronization, including explicit
URL commands. A separate request is required to reconnect it.

Obtain `youtube` from the operator's private remote or local source; do not guess a URL when no origin is configured. Missing selected renderer, service, video, or Python member paths can prevent workspace resolution.

```sh
mise exec -- bun install --frozen-lockfile
mise exec -- uv sync --locked
mise exec -- bun run test
```

Update tool configuration and `mise.lock` together only when changing tool versions. Do not regenerate lockfiles during routine setup.

## Inspect changes

```sh
bun run report:baseline
./scripts/update-subrepos.sh status
./scripts/update-subrepos.sh dry-run
git diff --check
git status --short
git status --ignore-submodules=none
```

Use `./scripts/update-subrepos.sh update` only for an actual update request after examining dry-run output and current child state. Investigate skips without resetting a repository.

## Scope checks to the change

```sh
bun run test
bun run test:changeset
bun run report:shared-ui
sh scripts/verify-all-web-ui-integration.sh
```

For changed shared UI consumers, choose affected `typecheck:web`, `test:web`, and `build:web` commands. The integration script's `--full` mode also requires installation, build, and registry access; prepare those prerequisites first. Do not make every child build a default root check.

For Python dependency changes, run the common checks, then only the affected package's tests:

```sh
uv run python scripts/verify-python-dependency-constraints.py
uv lock --check
uv run --package keelim-rich --group dev pytest rich/tests
uv run --package easy-release-note --group dev pytest youtube/tests
```

If the default cache is unavailable, pass `--cache-dir .omx/uv-cache` to uv. Explicitly name nested test paths outside an owner's default collection.

## Local tools

Use `bun run cg -- list` and `bun run cg:status` to locate owner indexes, then target a checkout, for example `bun run cg -- context rich "task description"`. Initialize a missing index only after confirming its installation and owner scope; never create an aggregate root source index.

`bun run automation:local -- list` and `status` inspect state. Mutation commands such as `start rich` or `stop n8n` name a runtime. `standby` stops Rich watchers and places Rich/n8n in standby while preserving agentgateway.

For a task requiring a Codex connection, run `bun run dev:codex-app-server`, then `codex --remote ws://127.0.0.1:7331` in another terminal. This starts a persistent server; do not include it in routine checks.

## Environment

| Setting | Purpose and scope |
| --- | --- |
| `NODE_AUTH_TOKEN` | Operator-supplied GitHub Packages read credential; never record its value |
| `CODEX_BIN` | Codex command or path used by the server helper |
| `CODEX_APP_SERVER_LISTEN` | Server transport address; default `ws://127.0.0.1:7331` |

Kubernetes, provider, and database credentials belong to their owning runtime and operator environment. There is no whole-root product deployment; use the owning repository's authorized release procedure.
