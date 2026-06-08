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
  - root local automation standby and local proxy removal requests.

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
   - Evidence: the June 5 local automation request moved from standby, to local
     proxy standby, to local proxy removal.
   - Small change: when the user changes an operation from "standby" to
     "remove", record the change as a new commit unit and preserve data-retention
     boundaries such as PVCs or secrets unless deletion is explicit.

## 2026-06-07 Follow-Up Evidence

- Product Design preflight still reports no saved
  `/Users/keelim/.codex/state/plugins/product-design/user-context.md`.
- Recent Codex session files since the previous automation marker numbered 183.
  Raw keyword scans over those JSONL logs were noisy because session files repeat
  base instructions, tool schemas, and plugin descriptions.
- The high-signal recent local artifacts were repo-backed rather than UI mocks:
  `docs/research/skillopt-integration-2026-06.md`,
  `docs/idea/net-new-2026-06-06.md`, root security/dependency scripts, and
  automation/process status outputs.

## 2026-06-07 Additional Improvements

7. Add a lightweight session-summary index before cross-session product analysis.
   - Evidence: 183 recent JSONL session files existed after the prior automation
     marker, and raw `rg` hits were polluted by repeated instructions.
   - Small change: build a local read-only summarizer that extracts session id,
     cwd, first user prompt, final outcome, tools used, and committed files before
     asking Product Design or service-improvement analysis to reason over sessions.

8. Treat Product Design mentions inside automation as insight mode by default.
   - Evidence: this run invoked `$product-design`, but the user asked for service
     improvements, not a visual brief, ImageGen options, or prototype build.
   - Small change: when Product Design is mentioned inside a repo-management
     automation, run context preflight and produce improvement artifacts only;
     do not enter image ideation unless the user supplies a concrete design target.

9. Save durable design context after repo-backed product decisions.
   - Evidence: Product Design context is still missing even though root docs now
     contain repeated decisions about `rich`, `youtube`, `keelim-vercel`, and
     shared UI surfaces.
   - Small change: after a design/product analysis run, offer one curated context
     bundle containing app paths, target surfaces, preferred verification commands,
     and active non-goals.

10. Distinguish product insight, runtime hygiene, and bug triage in automation
    reports.
    - Evidence: this recurring task combines commits, process cleanup,
      Product Design analysis, and recent-commit bug scanning; each has different
      proof requirements.
    - Small change: automation output should keep separate sections for
      `commits`, `processes`, `service improvements`, and `bug scan`, each with
      exact evidence and skipped/blocked items.

## 2026-06-08 Follow-Up Evidence

- Product Design preflight still reports no saved
  `/Users/keelim/.codex/state/plugins/product-design/user-context.md`.
- Raw cross-session search remains noisy: direct keyword scans over session JSONL
  match repeated system prompts, tool schemas, and old embedded session summaries.
  Chronicle 10-minute summaries are currently the higher-signal session layer.
- Recent session summaries after the previous automation run centered on:
  Naver Clip Creator upload/metadata handling, Easy Release Note motion-graphic
  variation, SkillOpt-style gated skill promotion, Rich local Kubernetes/admin
  verification, and a docs/words investing wiki ingest.
- The Naver Clip flow exposed an external-action risk: Chrome file-upload
  automation was blocked, manual file selection was needed, and live visibility
  settings could differ when reopening a draft.
- The YouTube SkillOpt video workflow exposed a design-quality risk: even
  source-correct videos can feel repetitive when the renderer reuses the same
  scaffold without a per-source visual grammar check.

## 2026-06-08 Additional Improvements

11. Use chronicle summaries as the default cross-session analysis layer.
    - Evidence: raw JSONL search returned repeated instructions and irrelevant
      old embedded summaries, while chronicle summaries named concrete workflows,
      files, blockers, and browser states.
    - Small change: Product Design/service analysis should first read a bounded
      chronicle index by timestamp, then open raw session logs only for a named
      thread or missing proof.

12. Add an external-action checkpoint for browser-backed publishing flows.
    - Evidence: Naver Clip upload/metadata sessions required manual file-picker
      selection, draft-save confirmation, and visibility-state checks before any
      registration action.
    - Small change: Product Design handoffs that cross into Chrome or creator
      studios should label steps as `local-prep`, `manual-upload`, `draft-save`,
      `visibility-check`, or `publish-authorized` and stop before publish unless
      explicitly authorized.

13. Track visual repetition risk before declaring a video/prototype done.
    - Evidence: the Easy Release Note SkillOpt episode was source-faithful but
      still needed a per-source render-layer pass because common scene scaffolding
      made the middle section feel too similar to prior videos.
    - Small change: add a lightweight `similarityRisk` field to Product Design
      and video-design handoffs, with one sentence comparing the output to the
      last few related artifacts.

14. Reuse gated promotion patterns for Product Design playbooks.
    - Evidence: recent SkillOpt work converged on ignored `.skillopt/` candidate
      storage, dry-run validation, `no-diff` semantics, and explicit `--apply`
      promotion rather than automatic skill overwrite.
    - Small change: Product Design prompt/playbook improvements should follow the
      same candidate -> validate -> inspect diff -> apply gate, especially for
      recurring workflows such as visual QA, session analysis, and publishing
      handoff checklists.
