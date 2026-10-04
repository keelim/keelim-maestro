# Workspace operating rules

## Ownership and membership

The root manages child projects without taking over their features, data, or release decisions. Assign every changed path to one owning repository. When providers and consumers differ, establish the delivery order before integrating their changes.

Git registration, package installation membership, and a convenience command are separate relationships. A command does not make its target a workspace member or submodule. Each product must retain instructions and configuration usable outside the parent checkout.

## Repository state and updates

A registered repository becomes a work target only when its checkout exists. Report absent optional repositories; do not clone or reactivate them from a historical reference alone. Archived `toto` requires an explicit reactivation request. Changes to `quant` remotes or registration also require a separate request.

Uncommitted changes, staged content, and unpublished commits belong to their authors. Do not reset them to make the workspace clean or to satisfy installation. If existing state blocks an update, skip the repository or report the reason.

Automatic updates are limited to clean supported branches that can fast-forward. Ahead or divergent history does not authorize rewriting or forcing alignment. Distinguish overall command success from skipped repositories.

## Meaning of completion

Registered, installed, implemented, check-passing, and operational are different states. Passing root checks does not validate Android apps, financial services, video uploads, or deployment. A connection indicator or health response alone does not prove a specific MCP method works.

A shared UI change is integrated only after the provider's public surface and affected consumers are verified. Building the provider alone does not establish consumer compatibility.

Research findings need real paths and evidence. Dated inventories describe observations, not current capabilities or priorities. Completed work requires an observable result and verification evidence.

Only approved documents enter the operator knowledge store. Inclusion in an input list does not prove retrieval readiness. Expansion of collection scope or movement to another database requires a confirmed destination and access boundary.
