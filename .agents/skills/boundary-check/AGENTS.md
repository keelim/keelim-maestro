# Repository boundary review

Inspect changed provider/consumer contracts and ownership read-only. Standalone review does not implement fixes, edit files, send external messages, or create a new work record.

- Start with changed public contracts and affected consumers; do not turn a focused review into an unrelated repository-wide issue inventory.
- Verify the provider, then affected consumers, using each owner's current checkout and commands.
- Use PASS for supported success, FAIL for a reproduced defect, and UNVERIFIED for environment, access, or service gaps. Access failure alone is not a product defect.
- Do not mix older handoff directories with the supplied run. Missing optional repositories and archived `toto` do not become active scope.
- Return defect paths, reproduction steps, and the smallest corrective action to the owner. The coordinator owns recording independent review results.

After skill edits, check input scope, verdict criteria, and result format for consistency. Keep Claude compatibility paths linked here. Do not claim discovery/invocation without a fresh-session check.
