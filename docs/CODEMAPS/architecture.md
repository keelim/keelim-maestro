# Architecture Codemap

<!-- Generated: 2026-08-31 -->

## Workspace Topology

```
keelim-maestro (superproject / coordination layer)
├── all               [submodule] Android app — Keelim "all" app
├── Keelim-Knowledge-Vault  [submodule] Knowledge/PKM vault
├── keelim-plugin     [submodule] Claude/Codex skill plugin (codemap generator, etc.)
├── keelim-vercel     [submodule] Vercel-deployed Next.js frontend
├── all-web-ui        [autonomous] Shared React/Tailwind UI component library
├── rich              [autonomous] Rich admin web + Python backend + open trading API
├── youtube           [autonomous] YouTube automation (Remotion, services, video projects)
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
| `Keelim-Knowledge-Vault` | Markdown / Obsidian | Knowledge vault (flat notes + metadata) |
| `keelim-plugin` | Python | Claude/Codex skills and automation scripts |
| `keelim-vercel` | Next.js / TypeScript | Full-stack web app (App Router, deployed to Vercel) |
| `all-web-ui` | React / TypeScript / Tailwind | Shared component library (publishes to GitHub Packages) |
| `rich` | Python + FastAPI + React | Admin web + algo trading + K8s local stack |
| `youtube` | TypeScript + Python | YouTube automation: Remotion renderer, services, video projects |

## Coordination Contracts

- **Bun workspace** — root install/lock surface for `all-web-ui`, `keelim-vercel`, `rich/web`, `youtube/*`
- **uv workspace** — root Python constraint surface for `rich` and `youtube`
- **Submodule pointers** — root gitlinks for `all`, `Keelim-Knowledge-Vault`, `keelim-plugin`, `keelim-vercel`
- **agentgateway** — shared local Kubernetes resource exposing MCP tools
- **GBrain** — knowledge system using a separate operator brain repo (`~/brain`); contract at `docs/knowledge/`

## Local Kubernetes Stack

| Runtime | Namespace | Start/stop |
| --- | --- | --- |
| `agentgateway` | fixed | `bun run automation:local -- start agentgateway` (always keep running) |
| `rich` (Skaffold) | on-demand | `bun run automation:local -- start rich` / `standby` |
