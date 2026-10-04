# Separate inspection from updates

## Context

Child repositories contain uncommitted work and unpublished commits belonging to different authors. A status query must not alter that work.

## Decision and alternatives

Keep inspection and preview read-only. Use a separate update action for eligible repositories. Automatic fetch, merge, or reset during reporting would mix observation with mutation.

## Consequences

Report success and update eligibility remain distinct. Cached remote tracking is not current server proof; skipped repositories are not repaired by forcing alignment.
