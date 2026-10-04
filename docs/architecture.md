# Workspace architecture

The root coordinates independently owned Git repositories. Shared installation and commands do not transfer ownership of a child's source, history, database, or release.

## Components and direction

| Component | Role and dependency direction |
| --- | --- |
| Root manifests and Git registration | Declare selected package membership and repository pins; child manifests retain package identity |
| `scripts/` | Read child state and delegate setup, checks, updates, and runtime control to the owning checkout |
| `scripts/improvements/` | Turn dated research inputs into reports and progress records; do not implement product changes |
| Shared workspace skills | Assign owners and review provider/consumer boundaries; do not create deployment authority |
| `docs/videos/subproject-intros/` | Converts local HTML and assets into previews and video; remains separate from product implementation |
| Android `all` | Owns applications, shared libraries, and platform builds independently of Bun and uv membership |
| `all-web-ui` → `keelim-vercel`, `rich/web` | Supplies React primitives, theme tokens, and public exports to two autonomous consumers |
| `rich`, `youtube` | Own finance and media products; participate in the declared Python and selected Bun workspaces |
| `keelim-plugin`, knowledge vault, `tools` | Own reusable skills, curated notes, and machine-local utilities respectively |
| Operator knowledge store | Receives selected documents outside product repositories; remains separate from product databases |

Bun coordinates the selected web and video packages. uv coordinates `rich` and `youtube`; the root Python project is not a distribution package. Android builds and product databases remain with their owners. Nested directories and convenience commands are not membership declarations.

## Representative flows

A cross-repository change goes from request scope to owner assignment, current-state inspection, provider implementation and checks, then consumer integration and checks. The changeset validator reads each owner's commit and check commands to validate the manifest; it does not execute those commands or rollback text.

A status request goes through a root command to registrations, manifests, and local child Git state, then returns a report. An update uses a separate command and processes only eligible repositories. Reading a report does not change source or Git pointers.

## External connections

Git remotes supply repository history. Public registries and GitHub Packages have different access requirements. Local workspace links and independent consumer installation both matter for the shared UI contract.

Managed local MCP connections use agentgateway as their ingress. Rich and n8n own their runtime lifecycles; GBrain belongs to the operator's knowledge environment. A root development command or Codex app-server helper does not create a public product API. A missing local gateway checkout does not establish the state of a separately running gateway.
