# Remove the root chart tool

## Context

The root contained a chart-to-video package and dedicated tests/docs. The user explicitly requested its removal while confirming the coordination role.

## Decision and alternatives

Remove source, dedicated documentation, commands, and installation registration together. Keeping it conflicts with the request; moving it into a child repository was not requested. Preserve the previous files in a local backup.

## Consequences

The root no longer provides those generation commands. Other video packages and ordinary chart features remain separate. A future tool request needs a new owner decision; this is not a permanent ban on video functionality.
