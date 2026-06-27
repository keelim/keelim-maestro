# Architecture Codemap

<!-- Generated: 2026-06-27 -->

## Workspace Topology

```
keelim-maestro (superproject / coordination layer)
├── all               [submodule] Android app — Keelim "all" app
├── android-support   [submodule] Android shared support library
├── Keelim-Knowledge-Vault  [submodule] Knowledge/PKM vault
├── keelim-plugin     [submodule] Claude/Codex skill plugin (codemap generator, etc.)
├── keelim-vercel     [submodule] Vercel-deployed Next.js frontend
├── toto              [submodule] KBO Streamlit dashboard (active Bun + uv workspace member)
├── all-web-ui        [autonomous] Shared React/Tailwind UI component library
├── rich              [autonomous] Rich admin web + Python backend + open trading API
└── quant             [autonomous, no remote] Quantitative research (excluded from root)
```

## MCP Routing Model

All MCP calls are modeled as passing through `agentgateway` regardless of agent type.
Agent type changes the execution role, not the MCP ingress path.

```
Agent (leader / subagent / worker / plugin)
    └─► agentgateway MCP  (http://localhost:3000/mcp)
            └─► MCP servers / tools
```

Codex and Claude Code use the shared `agentgateway` MCP endpoint at
`http://localhost:3000/mcp`. Document integrations behind `agentgateway` unless
a lower-level detail explicitly needs to be called out.

## Subproject Shapes

| Repo | Primary stack | Shape |
| --- | --- | --- |
| `all` | Android / Kotlin | Android app (multi-module Gradle) |
| `android-support` | Android / Kotlin | Android library (Gradle, detached at v0.0.8-4) |
| `Keelim-Knowledge-Vault` | Markdown / Obsidian | Knowledge vault (flat notes + metadata) |
| `keelim-plugin` | Python | Claude/Codex skills and automation scripts |
| `keelim-vercel` | Next.js / TypeScript | Full-stack web app (App Router, deployed to Vercel) |
| `toto` | Python / Streamlit | KBO baseball dashboard (29 files; Node/JavaScript + Python) |
| `all-web-ui` | React / TypeScript / Tailwind | Shared component library (publishes to GitHub Packages) |
| `rich` | Python + FastAPI + React | Admin web + algo trading + K8s local stack |

## Coordination Contracts

- **Bun workspace** — root install/lock surface for `all-web-ui`, `keelim-vercel`, `rich/web`, `toto`
- **uv workspace** — root Python constraint surface for `toto` and `rich`
- **Submodule pointers** — root gitlinks for `all`, `android-support`, `Keelim-Knowledge-Vault`, `keelim-plugin`, `keelim-vercel`
- **agentgateway** — shared local Kubernetes resource exposing MCP tools
- **GBrain** — knowledge system using a separate operator brain repo (`~/brain`); contract at `docs/knowledge/`

## Local Kubernetes Stack

| Runtime | Namespace | Start/stop |
| --- | --- | --- |
| `agentgateway` | fixed | `bun run automation:local -- start agentgateway` (always keep running) |
| `rich` (Skaffold) | on-demand | `bun run automation:local -- start rich` / `standby` |
