# Selected package membership

## Context

Web/video and Python packages benefit from shared dependency coordination; Android, archived material, and nested helpers are not the same installation unit.

## Decision and alternatives

Bun includes declared web/video paths; uv includes rich and youtube. Avoid recursive inclusion of every child path. Keep root constraints together with child direct dependencies and independent installation declarations instead of abandoning shared coordination.

## Consequences

Autonomous checkouts must be prepared before installation. Membership changes require aligned manifests, lockfiles, and bootstrap instructions; helper commands alone do not expand membership.
