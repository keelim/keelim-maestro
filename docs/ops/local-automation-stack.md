# Local Automation Stack Review

Date: 2026-05-31
Owner: `keelim-maestro` root coordination layer

This document is the root-owned audit for the local automation substrate around
`keelim-maestro`. It does not merge manifests or move runtime ownership. Each
runtime keeps its own repository, scripts, Kubernetes resources, and secret
handling; the root only documents the contracts and future orchestration shape.

## Current Dirty Boundaries

Observed before this document was added:

- `keelim-maestro` root: child repo entries were already modified for
  `Keelim-Knowledge-Vault`, `all`, `android-support`, `keelim-plugin`,
  `keelim-vercel`, and `toto`.
- `rich`: existing local K8s-related edits were already present in
  `.dockerignore`, `AGENTS.md`, `Dockerfile.k8s.backend.dev`,
  `tests/test_local_kubernetes_dev_artifacts.py`, and
  `tests/test_run_helper_scripts.py`; docs/words generated work was also dirty.
- `youtube`: `ops/n8n-k8s/README.md` and `ops/n8n-k8s/deployment.yaml` were
  already modified, and the checkout contained many untracked project artifacts.
- `tools/agentgateway`: clean at the time of review.

Do not normalize or discard any of those child-repo changes from the root. Enter
the child repo and follow its own `AGENTS.md` before changing child-owned files.

## Runtime Inventory

| Runtime | Owner | Kubernetes shape | Local ports | Primary role |
| --- | --- | --- | --- | --- |
| Rich local app | `rich` | Namespace `rich-local`, deployments `rich-backend` and `rich-frontend`, services on ports `8000` and `3000`, Skaffold-managed dev loop | `8000`, `3001` | On-demand FastAPI backend plus Next admin UI for local app debugging |
| n8n automation | `youtube` | Namespace `automation`, deployment `n8n`, service `n8n`, PVC `n8n-data`, task-runner sidecar | `5678` | On-demand workflow automation for upload jobs and update-tracker workflows |
| agentgateway MCP | `tools/agentgateway` | Namespace `agentgateway-local`, deployment/service `agentgateway-local`, custom local image | `3000`, `15000` | Fixed MCP ingress for Codex/app clients and remote Supabase, Lazyweb, and Stitch targets |
| GBrain knowledge layer | root docs + separate operator brain repo | PGLite smoke, later Postgres/Supabase brain | stdio MCP or remote HTTP MCP | Full-brain memory over curated workspace knowledge |

## Runtime Contracts

### Rich local app

- Owner files: `rich/run-k8s-dev.sh`, `rich/skaffold.yaml`,
  `rich/k8s/local/*`, `rich/Dockerfile.k8s.backend.dev`, and
  `rich/web/Dockerfile.k8s.dev`.
- Start: from `rich`, run `sh run-k8s-dev.sh` or `bun run dev:k8s`.
- Verify:
  - `kubectl -n rich-local get deploy,svc,pod`
  - `curl -fsS http://127.0.0.1:8000/healthz`
  - open `http://127.0.0.1:3001/admin`
- Stop: interrupt the foreground Skaffold loop; it owns cleanup for the local
  dev resources it started.
- Standby from the root: `scripts/local-automation.sh standby rich` stops any
  matching Rich Skaffold dev loop and scales `rich-backend` / `rich-frontend`
  deployments to `0` replicas if they still exist.
- Secrets and env: optional Kubernetes resources `rich-local-env` and
  `rich-local-secrets`. Do not commit Supabase, Google, KIS, Slack, or other
  real secret values into manifests, docs, or tests.
- Failure modes:
  - Passing manifest/unit tests is not proof that anything is running in the
    cluster. Check live `rich-local` resources separately.
  - A missing-env `/admin` 500 should be triaged through `rich-local-env`,
    `rich-local-secrets`, and pod env before changing app code.
  - Cold builds and steady-state save-triggered rebuilds have different timing;
    do not judge the edit loop only by first build timing.

### n8n automation

- Owner files: `youtube/ops/n8n/*`, `youtube/ops/n8n-k8s/*`,
  `youtube/src/easy_release_note/n8n.py`, and related tests under
  `youtube/tests/`.
- Start: from `youtube/ops/n8n-k8s`, use the documented `kubectl apply -k .`
  flow after ensuring the `automation` namespace and `n8n-secrets` exist.
- Verify:
  - `kubectl -n automation get pod,svc,pvc`
  - `kubectl -n automation logs deploy/n8n -c n8n --tail=80`
  - `kubectl -n automation logs deploy/n8n -c task-runners --tail=80`
  - `curl -fsSL --max-time 10 http://localhost:5678`
  - `kubectl -n automation exec deploy/n8n -c n8n -- test -d /data/easy-release-note/renders`
  - `kubectl -n automation exec deploy/n8n -c task-runners -- test -d /data/easy-release-note/renders`
- Stop without deleting data: `kubectl -n automation scale deployment/n8n --replicas=0`.
- Standby from the root: `scripts/local-automation.sh standby n8n` applies the
  same scale-to-zero behavior while preserving the namespace, PVC, Secrets, and
  manifests.
- Destructive removal: deleting namespace `automation` also removes the local
  runtime resources and may remove local data depending on the cluster/PVC
  implementation. Do not make this the default root stop behavior.
- Secrets and persistence:
  - Secret resource: `n8n-secrets` with `N8N_ENCRYPTION_KEY` and
    `N8N_RUNNERS_AUTH_TOKEN`.
  - Persistent data: PVC `n8n-data` mounted at `/home/node/.n8n`.
  - Host mount: `/Users/keelim/Desktop/keelim-maestro/youtube` mounted at
    `/data/easy-release-note` for workflow file access.
- Workflow contract:
  - Upload job generation stays in `uv run ern n8n export-upload-job`.
  - Workflow templates stay under `ops/n8n/workflows/`.
  - Runtime state and upload records stay under ignored n8n state/output paths.
- Failure modes:
  - `n8n execute --file` can collide with the running server task broker on
    port `5679`; prefer testing in the live n8n UI when the server is running.
  - Code nodes may restrict filesystem access unless the runtime explicitly
    allows needed modules. Keep file-writing responsibility aligned with the
    actual n8n runtime policy.

### agentgateway MCP

- Owner files: `tools/agentgateway/scripts/*`, `tools/agentgateway/k8s/*`, and
  ignored local secret files under `tools/agentgateway/secrets/`.
- Build image: from `tools/agentgateway`, run `./scripts/build-k8s-image.sh`.
- Start: `./scripts/start-k8s-gateway.sh`.
- Verify: `AGENTGATEWAY_URL=http://127.0.0.1:3000 ./scripts/verify-k8s-gateway.sh`.
- Stop: `./scripts/stop-k8s-gateway.sh --apply` to stop only matching
  Kubernetes `agentgateway` port-forwards.
- Standby from the root: `scripts/local-automation.sh standby` leaves
  `agentgateway` unchanged because it is the fixed MCP resource for this
  workspace. Stop it only with an explicit `scripts/local-automation.sh stop
  agentgateway` when MCP access should also be taken down.
- Ports:
  - `3000`: Codex/app and MCP endpoint, including `http://localhost:3000/mcp`.
  - `15000`: agentgateway admin UI port-forward.
- Secrets:
  - `supabase-mcp-authorization.txt`
  - `lazyweb-mcp-authorization.txt`
  - `stitch-mcp-authorization.txt`
  - Values remain in ignored local files and Kubernetes Secret
    `agentgateway-secrets`.
- MCP routing contract:
  - Supabase, Lazyweb, and Stitch MCP access should be documented and used
    behind `agentgateway` from this workspace.
  - Keep direct duplicate Supabase/Lazyweb registrations disabled when they
    would conflict with the gateway surface.
  - `omx_*` MCP registrations remain direct because they are local OMX runtime
    surfaces, not gateway targets.
- Failure modes:
  - If direct Lazyweb appears unavailable, check `agentgateway` before
    concluding the capability is absent.
  - If ports `3000` or `15000` are occupied, the start script exits before
    changing the port-forward. Stop the existing listener intentionally.

### GBrain knowledge layer

- Owner files: `docs/knowledge/*` and the separate operator brain repository
  such as `~/brain`.
- Start/install: follow `docs/knowledge/operator-runbook.md`; do not install,
  sync, migrate, or register cron jobs from the root helper.
- Verify:
  - `scripts/local-automation.sh status gbrain`
  - `scripts/local-automation.sh verify gbrain`
  - `gbrain doctor --json`
  - `gbrain stats`
  - one `gbrain search` and one `gbrain query` against root workspace topics
- MCP:
  - Local smoke may use `codex mcp add gbrain -- gbrain serve`.
  - Remote operation should use `gbrain connect ... --agent codex --install`
    with the bearer token kept in an environment variable.
- Secrets and persistence:
  - No provider keys, database URLs, bearer tokens, or local brain database files
    belong in the root repository.
  - The curated import pool and exclusions live in
    `docs/knowledge/source-targets.md`.
- Failure modes:
  - A passing root test does not prove GBrain is installed.
  - A registered MCP server is not proof of callability; verify
    `get_brain_identity`, `list_skills`, and one search/query call.
  - `gbrain sync` must be followed by `gbrain embed --stale` before treating new
    content as searchable through vector retrieval.

## Root Script Contract

The root has a coordination helper that delegates to existing runtime owners
instead of replacing them. Use it as a script index and conservative command
surface:

```text
scripts/local-automation.sh list [all|rich|n8n|agentgateway|gbrain]
scripts/local-automation.sh status [all|rich|n8n|agentgateway|gbrain]
scripts/local-automation.sh start <rich|n8n|agentgateway>
scripts/local-automation.sh verify [all|rich|n8n|agentgateway|gbrain]
scripts/local-automation.sh standby [all|rich|n8n|agentgateway]
scripts/local-automation.sh stop <rich|n8n|agentgateway>
```

Default behavior must be conservative:

- `list` is read-only and prints the owning script paths and command handoffs.
- `status` is read-only and reports Kubernetes resources plus relevant port
  listeners.
- `start` delegates to the runtime-owned command or documented `kubectl apply`
  flow.
- `verify` runs the runtime-owned health checks listed above.
- `standby` keeps `agentgateway` fixed and unchanged while stopping on-demand
  runtimes. For `rich`, it stops only matching `skaffold dev --filename
  .../rich/skaffold.yaml` processes and then scales remaining Rich deployments
  to zero. For `n8n`, it scales `deployment/n8n` to zero.
- `stop` is scoped and non-destructive by default. It may stop foreground
  port-forwards or scale a deployment to zero, but it must preserve PVCs,
  Secrets, and manifests unless a later explicit `destroy` command is approved.
- `gbrain` supports only `list`, `status`, and `verify`; install, sync,
  migration, cron, and MCP registration stay explicit operator actions.

Suggested status probes:

```bash
kubectl get ns rich-local automation agentgateway-local
kubectl -n rich-local get deploy,svc,pod
kubectl -n automation get deploy,svc,pvc,pod
kubectl -n agentgateway-local get deploy,svc,pod
lsof -nP -iTCP:3000 -sTCP:LISTEN
lsof -nP -iTCP:3001 -sTCP:LISTEN
lsof -nP -iTCP:5678 -sTCP:LISTEN
lsof -nP -iTCP:8000 -sTCP:LISTEN
lsof -nP -iTCP:15000 -sTCP:LISTEN
```

## Validation Plan

For this audit document, validation stays read-only:

```bash
bun run report:baseline
bun run test
sh scripts/local-automation.sh list
git status --short
git -C rich status --short
git -C /Users/keelim/Desktop/keelim-maestro/youtube status --short
git -C tools/agentgateway status --short
```

Only run live cluster checks when an active Kubernetes context is intentional.
Do not start or stop `rich`, n8n, or `agentgateway` from root documentation work
unless explicitly requested.
