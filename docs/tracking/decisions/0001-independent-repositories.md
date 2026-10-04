# Independent child ownership

## Context

Shared setup is needed across products with separate Git histories and release boundaries. The user confirmed that the root coordinates the child projects.

## Decision and alternatives

Keep implementation and releases with each owner and coordinate shared contracts at the root. Consolidating source/history would change independent clone and deployment boundaries; removing all coordination would lose provider/consumer delivery ordering.

## Consequences

Preserve and verify each owner separately. Root success cannot establish product completion or authorize resetting siblings.
