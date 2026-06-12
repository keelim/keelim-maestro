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

## 2026-06-09 Follow-Up Evidence

- Product Design preflight still reports no saved
  `/Users/keelim/.codex/state/plugins/product-design/user-context.md`.
- Chronicle summaries after the previous automation run show Work Relay moving
  from a broad "reduce work time by 50%" idea into a Product Design brief for a
  Korean-first Rich admin surface around `/admin/work-triage` and proposed
  `/admin/ops`.
- The visible Work Relay UI evidence centered on a signal inbox, evidence
  preview, Action Packet panel, risk boundary, required proof checklist, and
  time-saved metrics.
- SkillOpt production moved through Google Vids voiceover export, Remotion audio
  attachment, EN/KO validation, YouTube Studio metadata/playlist checks, and
  Naver Clip draft/upload-state checks.
- Rich Stitch work synchronized route captures to an existing Stitch project
  with local `.stitch` artifacts, dry-run defaults, explicit approval for
  external sync, sensitive-content audit, and route-map reconciliation.
- A separate Google Stitch session generated all-web-ui component/system
  variants in browser state, including blueprint/editorial/SaaS directions,
  without a saved Product Design context file.

## 2026-06-09 Additional Improvements

15. Persist Product Design brief decisions before retrying build or ideation.
    - Evidence: Work Relay was blocked on Product Design brief approval, then a
      retry path treated the brief as baseline and continued.
    - Small change: write the accepted brief, target route, visual source, and
      non-goals into a repo or Product Design context artifact before generating
      variants or starting implementation.

16. Make Action Packet plus Proof Bundle the default Product Design handoff shape
    for Work Relay-style products.
    - Evidence: the visible `/admin/ops` Work Relay concept already organized
      signals into evidence previews, risk boundaries, required proof, and a
      next-action button.
    - Small change: design handoffs for operations consoles should include
      `signal`, `evidence`, `riskBoundary`, `requiredProof`, `owner`, and
      `nextAction` fields.

17. Add a media-production quality gate for Product Design/video workflows.
    - Evidence: the SkillOpt Korean Google Vids voiceover first exceeded the
      Shorts target and had to be shortened before final Remotion validation.
    - Small change: require duration, audio codec/sample-rate, loudness,
      safe-area frame checks, and similarity-risk notes before a video/prototype
      is marked ready.

18. Treat external design sync as an approval-gated publish step.
    - Evidence: the Rich Stitch workflow used local `.stitch` captures, dry-run
      behavior, sensitive-content audit, explicit approval, and remote route-map
      reconciliation against an existing project.
    - Small change: Product Design share/sync workflows should label local
      capture, privacy audit, dry run, external upload approval, remote id
      reconciliation, and rollback notes separately.

19. Track cross-posting state per platform instead of a single "published" flag.
    - Evidence: the SkillOpt package had YouTube private upload plus playlist
      state, while Naver Clip moved through upload, draft/edit, visibility, and a
      cancel-unsaved modal.
    - Small change: store per-platform states such as `local-rendered`,
      `uploaded-private`, `draft-saved`, `visibility-checked`,
      `playlist-attached`, and `publish-performed`.

20. Save reusable design-system exploration into durable Product Design context.
    - Evidence: a Google Stitch all-web-ui component map and multiple generated
      variants existed in browser/design-tool state while Product Design saved
      context remained missing.
    - Small change: after design-system exploration, save the chosen component
      map, rejected directions, visual rules, and share target into Product
      Design context or repo `DESIGN.md`.

## 2026-06-12 Follow-Up Evidence

- Product Design preflight still reports no saved
  `/Users/keelim/.codex/state/plugins/product-design/user-context.md`.
- Chronicle summaries after the previous automation run show a
  `subproject-improvements-html-report` task aimed at an 800-item improvement
  backlog across 8 subprojects, using the existing
  `keelim-plugin/skills/html-report-generator` renderer.
- The current repo state contains partial raw improvement inputs and helper
  scripts under `docs/research/improvements-2026-06/` and
  `scripts/improvements/`, but the planned final outputs
  `improvements.json`, `report-input.json`, `improvement-items-2026-06.html`,
  and `improvement-items-2026-06.md` are not present.
- The same session showed a separate Fable video-production task moving through
  source browsing, package preparation, Remotion scene checks, Google Vids
  voiceover outputs, and per-platform upload/draft-state planning.
- The generated raw improvement inputs include `debug-log.json` residue, which
  reinforces the need to keep agent scratch/debug artifacts out of product
  evidence packages.

## 2026-06-12 Additional Improvements

21. Mark cross-project improvement backlogs as staged until final counts render.
    - Evidence: the Chronicle plan targeted 100 items per 8 projects, but the
      repo currently has only partial raw files plus scripts and no final
      `improvements.json` or report artifact.
    - Small change: Product Design and report-generation handoffs should expose
      `raw-collected`, `aggregated`, `validated`, `rendered`, and `ready`
      statuses instead of a single done/undone state.

22. Add a hard artifact-readiness gate before service insights are promoted.
    - Evidence: helper scripts exist for aggregation and count checks, while the
      final HTML/Markdown outputs are missing.
    - Small change: do not cite or commit a large improvement report as an
      output until `check_counts.py` passes and the renderer produces both the
      HTML report and Markdown summary.

23. Treat local file-path evidence as the shared currency between Product
    Design, bug triage, and backlog reports.
    - Evidence: the improvement-report plan required repository-relative file
      paths, severity mapping, and no remote URL leakage; the recurring bug
      scan requires concrete SHA/file/diff/test evidence.
    - Small change: add an `evidenceRefs` shape with `repo`, `path`, optional
      `commit`, `testCommand`, and `status` fields to Product Design handoffs
      that feed engineering work.

24. Keep generated debug artifacts out of durable design and research packages.
    - Evidence: `debug-log.json` appears in root and child dirty states and also
      inside `docs/research/improvements-2026-06/raw/`.
    - Small change: add a reject rule for debug/session hook artifacts before
      aggregation, and summarize them only as process residue in automation
      reports.

25. Connect source-backed video tasks to the same publish-state model as Product
    Design external sync.
    - Evidence: the Fable production path touched Chrome source review,
      package files, Remotion props, Google Vids voiceover exports, Naver Clip
      prep, and explicit no-upload/no-registration states.
    - Small change: use one platform-state checklist for creator workflows:
      `source-checked`, `local-rendered`, `voiceover-attached`,
      `frame-reviewed`, `uploaded-private`, `draft-saved`,
      `visibility-checked`, and `publish-authorized`.

## 2026-06-12 GBrain Follow-Up Evidence

- Product Design preflight still reports no saved
  `/Users/keelim/.codex/state/plugins/product-design/user-context.md`.
- Recent Chronicle/memory evidence after the previous automation marker shows a
  GBrain knowledge-layer rollout that converged on a root-owned contract,
  separate operator brain repository, local PGLite smoke first, and later
  Postgres/Supabase promotion only after credentials and destination are
  verified.
- Current root docs under `docs/knowledge/` and `docs/ops/local-automation-stack.md`
  separate documentation, install, sync, migration, cron, MCP, and secret
  boundaries instead of treating "GBrain exists" as a single completed state.
- `scripts/local-automation.sh status gbrain` can prove CLI availability and
  local docs presence, but the verification contract still requires MCP tool
  calls and search/query proof before the brain is considered ready.

## 2026-06-12 GBrain Improvements

26. Model knowledge-layer adoption as an explicit readiness ladder.
    - Evidence: the GBrain rollout distinguishes local docs, PGLite smoke,
      curated import, Postgres/Supabase promotion, MCP registration, and MCP
      callability.
    - Small change: Product Design and service handoffs for agent memory should
      use states such as `documented`, `local-smoke`, `curated-imported`,
      `remote-promoted`, `mcp-registered`, and `mcp-call-verified`.

27. Add a credential-destination preflight before operator-plane mutations.
    - Evidence: GBrain migration is blocked until provider/database credentials
      and the external destination are verified, and the repo docs explicitly
      keep database URLs, bearer tokens, and provider keys out of git.
    - Small change: before install, migration, cron, sync, or external MCP setup,
      require a short preflight that names the destination, secret location, and
      rollback artifact without printing secret values.

28. Treat MCP registration as incomplete until a tool-call proof bundle exists.
    - Evidence: the GBrain verification contract requires identity, skill-list,
      and search/query calls; status output alone only shows version, docs, and
      local environment hints.
    - Small change: every Product Design or automation handoff involving MCP
      should attach a proof bundle with `server`, `transport`, `toolCalls`,
      `resultSummary`, and `missingProof` fields.
