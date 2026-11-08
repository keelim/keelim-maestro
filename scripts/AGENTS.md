# Workspace command helpers

Own workspace inspection, installation/check delegation, updates, and runtime control. Child implementations, databases, credentials, and release procedures remain with their owners. Dated research tools have a separate boundary in `improvements/`.

- Resolve the Git root and name each child command target. Do not edit child source through a helper as a side effect.
- Keep `status`, `dry-run`, baseline, and contract reporting free of source/gitlink mutations. Report production is not check success.
- Update only clean supported branches by fast-forward. Skip local changes/commits; do not recover with resets.
- Delegate runtime actions to owner commands. `start`/`stop` require one target; `standby` preserves agentgateway.
- Handle spaces, symlinks, and path escape in user input. Validating a changeset command must not execute its string as shell code.
- Do not silently initialize indexes or restore archived `toto`. Report absent optional checkouts.

After behavior changes run root `bun run test` and `git diff --check`. Parser changes also need `bun run test:changeset` coverage for escaped paths, dirty state, HEAD mismatch, duplicate order, and invalid commands. Verify that callers can distinguish report-level failure from process failure. Start runtimes or build products only when the changed behavior needs that verification.
