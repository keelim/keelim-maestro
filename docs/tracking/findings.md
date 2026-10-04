# Unresolved findings

## Historical intro video differs from the active inventory

`docs/videos/subproject-intros/index.html` still contains scenes for absent `android-support` and archived `toto`. Reusing it as a current introduction can imply those projects are active. Video content and timing changes are outside the current documentation and root-tool-removal scope. Before reuse, reconcile scenes, captions, and the closing inventory with current ownership, then verify the render.

## Child state prevents reproducible pinning

The baseline report observed dirty worktrees, absent upstreams, divergent history, and no `youtube` origin. Pinning through these conditions can omit unpublished work or make a fresh clone irreproducible. Resolving another owner's changes/history is outside this work. Confirm intended commits and remotes with their owners before refreshing the baseline and pinning.

## Local gateway source is absent

The autonomous `tools` worktree currently has tracked `agentgateway` files deleted. Root helpers that reference those paths cannot be assumed runnable from this checkout. Preserve the deletion; restoring or replacing the gateway needs an explicit owner decision. A separately running service or host-provided MCP tool does not prove that the local source paths exist.
