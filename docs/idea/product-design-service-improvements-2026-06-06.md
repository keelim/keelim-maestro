# Product Design Service Improvements - 2026-06-06

## Evidence Scope

- Product Design plugin context preflight returned no saved `user-context.md`.
- `MEMORY.md` records the June 4 Rich admin redesign as a Product Design run:
  it used a direction gate, selected option 1, changed admin shell/global
  styling, and remained partially verified because the local runtime was down.
- Recent Codex sessions since the previous automation run covered:
  - project-management automation in an unhydrated Codex worktree,
  - local Kubernetes/OrbStack and Rich readiness triage,
  - Threads crawling for short-form content analysis,
  - Bedrock/Codex video workflow work,
  - root local automation standby and Headroom removal requests.

## Improvements

1. Add a Product Design context setup nudge after any design run with missing
   saved context.
   - Evidence: Product Design preflight reported
     `/Users/keelim/.codex/state/plugins/product-design/user-context.md` as
     missing.
   - Small change: after a successful or partial design run, offer to save the
     target app path, selected visual direction, design-system references, and
     preferred verification route.

2. Track design verification status as a first-class handoff field.
   - Evidence: the Rich admin Product Design memory says the black-console
     implementation stayed partial because visual verification was incomplete.
   - Small change: each design run should end with one of `visual-verified`,
     `runtime-blocked`, or `not-built`, plus the exact missing command or URL.

3. Detect unhydrated superproject worktrees before repo-management automation.
   - Evidence: automation memory shows repeated pivots from Codex worktrees to
     `/Users/keelim/Desktop/keelim-maestro`; the 2026-06-06 run repeated this.
   - Small change: make the project-management automation start with a
     hydration probe for `tools/`, `rich/`, and real child `.git` directories,
     then pivot once without re-discovering the same failure.

4. Prefer short, resumable browser extraction batches for social/profile
   crawling.
   - Evidence: the June 5 Threads session repeatedly hit long Chrome
     evaluation calls and had to shrink extraction batches.
   - Small change: profile crawlers should store progress after each small
     scroll batch and avoid whole-page `innerText` reads.

5. Separate local runtime state from repository implementation state in status
   reports.
   - Evidence: recent sessions mixed Kubernetes pod readiness, local
     port-forward availability, and repo dirty-state decisions.
   - Small change: reports should label `repo`, `kubernetes`, `port-forward`,
     and `browser-verification` separately so a runtime outage does not look
     like an implementation failure.

6. Keep scope-change handling explicit for operations requests.
   - Evidence: the June 5 local automation request moved from standby, to
     Headroom standby, to Headroom removal.
   - Small change: when the user changes an operation from "standby" to
     "remove", record the change as a new commit unit and preserve data-retention
     boundaries such as PVCs or secrets unless deletion is explicit.
