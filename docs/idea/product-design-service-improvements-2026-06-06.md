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

## 2026-06-15 Follow-Up Evidence

- Product Design context preflight still has no saved
  `/Users/keelim/.codex/state/plugins/product-design/user-context.md`, and this
  run did not expose a callable Product Design MCP tool through tool discovery.
- The June 14 Easy Release Note session added a repo-local concept-selection
  gate after the user said the generated videos felt too similar. The durable
  rule now chooses among `source-scanner`, `workflow-desk`,
  `product-spotlight`, and `impact-radar` before renderer selection.
- The same video workflow made concept selection affect actual Remotion props or
  HyperFrames HTML/GSAP structure, not only package prose.
- The `codex-reset-banking` production pass synced episode metadata to verified
  YouTube Studio state only after EN voiceover muxing, private upload proof,
  checks status, AI disclosure, save state, and visibility were recorded.
- The June 14 `라오어 무한 매수법` research session used source-backed Korean
  evidence, an explicit `autoresearch-goal` slug, a saved `research.md`, and a
  completion snapshot before treating the work as durably complete.
- The current root worktree also contains untracked automation/project artifacts
  such as `ORIGINAL_REQUEST.md`, `PROJECT.md`, and ignored pytest reports, which
  are useful run context but should not become durable product evidence unless
  deliberately routed.

## 2026-06-15 Additional Improvements

29. Make concept choice a first-class Product Design primitive.
    - Evidence: Easy Release Note quality improved by inserting concept
      selection before renderer choice, with four fixed visual-world options and
      a selected-concept record.
    - Small change: Product Design handoffs should ask for a visual-world or
      workflow concept before prototype generation when repeated outputs risk
      looking alike.

30. Require concept decisions to change implementation structure.
    - Evidence: the release-note workflow now says selected concepts must affect
      renderer mix, motion preset, layout, source signal, media, data, theme, or
      HTML/GSAP structure.
    - Small change: design handoffs should include a `conceptImpact` checklist
      and reject outputs where the concept appears only in copy or filenames.

31. Attach platform-state proof before syncing creator metadata.
    - Evidence: `codex-reset-banking` local manifests were updated only after
      YouTube Studio showed the uploaded file, private visibility, AI
      disclosure, category, checks, restrictions, and disabled Save state.
    - Small change: creator Product Design workflows should require
      `platform`, `asset`, `visibility`, `checks`, `saveState`, and
      `externalUrl` proof fields before marking upload metadata synced.

32. Keep automation project files in a declared run-artifact lane.
    - Evidence: `ORIGINAL_REQUEST.md`, `PROJECT.md`, and pytest reports are
      present as useful automation context but are not inherently root-owned
      service-improvement outputs.
    - Small change: recurring project-management runs should label generated
      artifacts as `scratch`, `report`, `ledger`, or `durable-doc` before any
      commit decision.

33. Use completion snapshots for source-backed research handoffs.
    - Evidence: the LAOO research flow avoided a false finish by saving a fresh
      Codex completion snapshot and reconciling it through the OMX
      `autoresearch-goal complete` command.
    - Small change: research-oriented Product Design or service-analysis tasks
      should keep `sourceSet`, `verdict`, `completionSnapshot`, and
      `openQuestions` fields together in the final handoff.

## 2026-06-27 Follow-Up Evidence

- Product Design preflight still found no saved
`/Users/keelim/.codex/state/plugins/product-design/user-context.md`, and
tool discovery exposed Lazyweb tools rather than a Product Design-specific
MCP surface.
- The 2026-06-25 Codex App usage session separated Desktop UI visibility
from Headroom proxy/runtime proof: config pointed at `127.0.0.1:8787/v1`,
Headroom had request/savings evidence, but the app usage surface still did
not show the expected result.
- Recent wiki sessions in `rich` / `words` stored raw Korean trading notes,
then converted them into reusable wiki pages or a five-gate same-day stock
selection abstraction.
- The 2026-06-26 `rich` wiki ingestion session showed a duplicated title
/ stretched-content artifact that had to be manually cleaned before
`wiki_refresh` and `wiki_lint` could be trusted.
- The `TauricResearch/TradingAgents` review context emphasized financial
agent nondeterminism: live data, LLM sampling, and reasoning-model behavior
can vary even with similar prompts.

## 2026-06-27 Improvements

34. Split UI-visible status from runtime proof in service handoffs.
- Evidence: Codex App usage analysis had real Headroom config and proxy
activity evidence, while the Desktop usage display remained unclear.
- Small change: Product Design/service handoffs should report `uiVisible`,
`runtimeCallable`, `dataObserved`, and `userExpectation` separately.

35. Preserve specific notes and reusable abstractions together.
- Evidence: Korean day-trading work needed both raw wiki capture and the
five-gate generalized stock-selection framework.
- Small change: session-to-service analysis should keep `rawNote`,
`normalizedPattern`, and `reusePrompt` fields when turning one-off knowledge
into product guidance.

36. Validate generated wiki text before treating lint as final.
- Evidence: `rich` wiki ingest duplicated/stretched the title/content, and
manual cleanup was required before final wiki checks were meaningful.
- Small change: add a pre-lint text-integrity check for duplicate headings,
repeated paragraphs, and source-reference preservation.

37. Make financial-agent reproducibility an explicit gate.
- Evidence: `TradingAgents` repo review context called out LLM sampling,
live data changes, and reasoning-model nondeterminism.
- Small change: financial research agent outputs should include
`dataSnapshot`, `modelConfig`, `rerunVariance`, and `claimGrounding` before
being promoted into product backlog or trading guidance.

38. Treat install/reload states as first-class plugin setup proof.
- Evidence: harness setup work moved through plugin install, reload, skill
/ agent counts, then project-local exploration before planning.
- Small change: agent/team setup handoffs should record `installed`,
`reloaded`, `capabilitiesObserved`, and `projectFitChecked` rather than a
single "setup done" flag.

## 2026-06-28 Correction

- Recent commit `91369fa` added the 2026-06-27 section, but parts of items 36-38 are hard to review because several sentences were compressed into one paragraph. Treat the normalized wording below as the current readable version of those items.
- Item 36: generated wiki text needs a pre-lint text-integrity check for duplicate headings, repeated paragraphs, and source-reference preservation.
- Item 37: financial research agent outputs need `dataSnapshot`, `modelConfig`, `rerunVariance`, and `claimGrounding` before promotion into product backlog or trading guidance.
- Item 38: plugin or agent setup handoffs need `installed`, `reloaded`, `capabilitiesObserved`, and `projectFitChecked` rather than a single "setup done" flag.

## 2026-06-28 Follow-Up Evidence

- Product Design preflight still reports missing `/Users/keelim/.codex/state/plugins/product-design/user-context.md`.
- Since the 2026-06-27T00:01:50Z automation marker, root commit `91369fa` only changed this service-improvement document; no child repo had a newer commit in `git log --since`.
- `tools/codex-hygiene/codex-hygiene.sh --dry-run` found no runaway native-hook scans; it reported one Codex stdio app-server process and no `node_repl` residue.
- `rich` and `youtube` currently have broad dirty trees, while `all-web-ui` only has untracked `debug-log.json`; these are not safe automatic commit units.
- Chronicle evidence for TradingAgents split provider quota/rate-limit failures from graph bugs, and split Headroom's OpenAI-compatible HTTP endpoint from Codex app-server's WebSocket turn protocol.
- Chronicle evidence for the YouTube Easy Release Note harness showed four `.claude/agents/*` files plus `.claude/commands/youtube-create.md`, reusing existing repo assets and avoiding new production code.

## 2026-06-28 Improvements

39. Classify repo sweep state before any automated commit.
- Evidence: current root status has a small uv constraint diff, broad mixed `rich` and `youtube` changes, `Keelim-Knowledge-Vault` pointer movement, and scratch artifacts such as `.coverage`, `ORIGINAL_REQUEST.md`, `PROJECT.md`, `reports/`, and `debug-log.json`.
- Small change: commit automation should label each candidate `commit-ready`, `mixed-user-work`, `scratch`, or `submodule-pointer` before staging files.

40. Split provider, protocol, and product-result proof for agent integrations.
- Evidence: TradingAgents work had Gemini `429` quota evidence, Headroom `/v1` HTTP compatibility, Codex app-server WebSocket incompatibility, and market-only smoke outcomes as separate facts.
- Small change: agent-integration handoffs should record `providerState`, `endpointProtocol`, `marketSmokeResult`, and `structuredOutputStatus` separately.

41. Make creator harness setup proof asset-based.
- Evidence: the YouTube harness was useful because it reused `AGENTS.md`, the Easy Release Note workflow skill, `platform-prep.md`, and the object-character prompt skill rather than creating a second production pipeline.
- Small change: creator workflow setup should include `reusedAssets`, `newCoordinationFiles`, and `productionCodeChanged` fields.

42. Keep Product Design context absence as a health flag, not a repeated finding.
- Evidence: multiple automation runs still find no saved Product Design `user-context.md`.
- Small change: service-improvement runs should report the missing context once per run as `productDesignContext=missing`, then spend analysis budget on new session evidence.

## 2026-06-29 Follow-Up Evidence

- Product Design context remains missing: `/Users/keelim/.codex/state/plugins/product-design` does not exist in this run.
- Since the 2026-06-28T00:01:22Z automation marker, 18 Codex JSONL session files existed under `/Users/keelim/.codex/sessions/2026/06/28` and `/Users/keelim/.codex/sessions/2026/06/29`; several were approval-review or subagent transcripts rather than user-facing product work.
- Chronicle evidence for YouTube Studio metadata work showed separate states for reference-short selection, draft metadata editing, save uncertainty, and local repo note sync.
- Chronicle evidence for Google Docs/Medium writing showed the user moving Korean draft material through cleanup and translation while monitoring multiple agent jobs and session-management reflections.
- Chronicle evidence for Google Drive / Google Vids export showed direct Drive download returning HTML, unavailable Chrome DevTools port `9222`, a hung browser download event, and a failed local `say` TTS fallback.
- Chronicle evidence showed macOS application-memory pressure pausing Codex around 10 GB and Chrome around 3.84 GB while the user monitored concurrent agent work.

## 2026-06-29 Improvements

43. Classify session records before product analysis.
- Evidence: recent session files mixed user sessions, automation runs, approval-review transcripts, and subagent outputs; unfiltered parsing surfaced giant embedded transcripts rather than service signals.
- Small change: session-analysis tools should tag each record as `humanTask`, `automation`, `approvalReview`, or `subagent` before summarizing product learnings.

44. Track browser-edit proof states separately.
- Evidence: YouTube Studio metadata work required distinguishing high-view reference selection, draft-field edits, actual Studio save, and local note sync.
- Small change: browser-backed editing handoffs should expose `referenceChosen`, `draftEdited`, `remoteSaved`, and `localSynced` instead of one `done` flag.

45. Add authenticated media export proof fields.
- Evidence: Google Drive / Vids export attempts failed in different ways: HTML download response, unavailable DevTools, hung download event, and zero-duration local TTS fallback.
- Small change: media-production workflows should record `sourceApp`, `downloadMethod`, `fileVerified`, `fallbackTried`, and `remainingBlocker`.

46. Surface local resource pressure in multi-agent dashboards.
- Evidence: Chronicle captured macOS pausing Codex and Chrome under memory pressure while several agent jobs were active.
- Small change: agent dashboards should show `appMemoryPressure`, `pausedApps`, and `restartSuggested` alongside task status so operator time is not spent debugging stalled agents as product failures.

## 2026-07-02 Follow-Up Evidence

- Product Design plugin package is installed (`product-design` 0.1.47), but no saved Product Design user context was found under `/Users/keelim/.codex/state/plugins/product-design`.
- Since the previous project-management automation marker, the high-signal new session summary is the Rich daily market snapshot run in `/Users/keelim/Desktop/keelim-maestro/rich`.
- That run collected `2026-06-29`, `2026-06-30`, and `2026-07-01`, skipped `2026-06-27` and `2026-06-28` with `PYKRX_DAILY_SNAPSHOT_UNAVAILABLE` quality reasons, and verified persistence with `DailyMarketSnapshotStore().list_snapshot_dates()`.
- The first `uv run` attempt failed before Python startup because `/Users/keelim/.cache/uv` was not accessible in the sandbox; rerunning with the allowed cache/escalation path recovered the task.

## 2026-07-02 Improvements

47. Split command success from durable store proof.
- Evidence: Rich snapshot collection was only accepted after `DailyMarketSnapshotStore().list_snapshot_dates()` returned dates through `2026-07-01`.
- Small change: data-producing automations should expose `commandSucceeded`, `storeVerified`, and `verifiedRecords` separately.

48. Preserve no-data quality reasons in operator-facing results.
- Evidence: collector skipped `2026-06-27` and `2026-06-28` as `PYKRX_DAILY_SNAPSHOT_UNAVAILABLE` with `all_zero_market_totals` and `all_zero_top_movers`; user explicitly required no fabricated backfill dates.
- Small change: market/data workflows should show `skippedDates`, `qualityReasons`, and `fallbackAttempted=false` in the final handoff.

49. Classify runner failures before product failures.
- Evidence: `uv run` failed on cache initialization before app code ran, then succeeded through the permitted cache/escalation path.
- Small change: automation reports should label failures as `runnerBlocked`, `providerBlocked`, `appFailed`, or `dataUnavailable` before proposing fixes.

## 2026-07-05 Follow-Up Evidence

- Process hygiene stayed script-first: sandboxed process-table read failed, then `tools/codex-hygiene/codex-hygiene.sh --dry-run` reported no runaway native-hook scans, `node_repl=0`, and stdio app-server `count=0`.
- Commit automation found verified child units and made unsigned local commits because each checked repo had `commit.gpgsign=true`, `gpg.format=ssh`, and the SSH signing key passphrase was unavailable in the agent session.
- Codebase-memory coverage was uneven: current indexed projects included only root, `all`, and `all-web-ui`; `rich` needed a fresh fast index before weekly-review API contract analysis.
- `rtk read`/`rtk proxy` compressed Kotlin syntax enough to hide operators such as expression-body `=` and matcher calls, so syntax-sensitive review relied on Gradle tests/build rather than compressed file display.
- `docs/research/product-design-subproject-opportunities-2026-07-04.md` is explicitly a lightweight, non-screenshot-backed Product Design triage; current `rich` Stitch route-map entries for new money screens remain `pending-capture`.
- Local/generated residue remains common across child repos: `.serena/`, `debug-log.json`, `web/next-env.d.ts`, and `web/tsconfig.tsbuildinfo` were left uncommitted unless they belonged to a verified meaningful unit.

## 2026-07-05 Improvements

50. Add graph coverage preflight before cross-repo analysis.
- Evidence: root codebase-memory project was too small for child implementation work, and `rich` had to be indexed on demand before inspecting `WeeklyReviewGenerateAIResponse`.
- Small change: service-analysis runs should report `graphProject`, `rootPath`, `nodes`, `edges`, `childCoverage`, and `fallbackUsed` before relying on graph answers.

51. Add syntax-sensitive read mode to RTK-guided workflows.
- Evidence: compressed command output obscured Kotlin syntax while `:app-arducon:testDebugUnitTest` and `:app-arducon:assembleDebug` proved the code actually compiled.
- Small change: when reviewing code syntax, commands should switch to an explicit unfiltered read/build proof lane and label compressed output as summary-only.

52. Make commit-signing status first-class in automation handoffs.
- Evidence: `all`, `all-web-ui`, and `rich` all required unsigned fallback commits because SSH signing requested a passphrase.
- Small change: commit automation should record `signingConfigured`, `signed`, `fallbackUnsigned`, and `reason` per repo.

53. Separate Product Design triage from screenshot-backed audit.
- Evidence: the 2026-07-04 Product Design subproject report names itself lightweight and not screenshot-backed, while new `rich` route-map targets still need captures.
- Small change: Product Design outputs should carry `triage`, `screenCaptured`, `mockupReviewed`, and `implementationVerified` states.

54. Classify local tooling residue before staging.
- Evidence: `.serena/`, `debug-log.json`, generated Next files, and broad YouTube render/package changes repeatedly appear beside real source changes.
- Small change: repo sweep UI should bucket dirty files as `commitReady`, `generated`, `toolResidue`, `broadProductionBatch`, or `needsHumanGrouping` before staging.

## 2026-07-08 Follow-Up Evidence

- Product Design context remains absent: `/Users/keelim/.codex/state/plugins/product-design` did not exist during this run.
- Tool discovery for `$product-design` exposed Creative Production widgets and unrelated session/process tools, but no callable Product Design analysis tool in the current surface.
- Since the 2026-07-07T14:21:54Z automation marker, session search found current automation/self-review JSONL files under `/Users/keelim/.codex/sessions/2026/07/07` and `/Users/keelim/.codex/sessions/2026/07/08`; one approval-review subagent transcript existed solely to approve `codex-hygiene.sh --dry-run`.
- Reading those JSONL files naively pulled the current run's prompt, tool calls, approval transcript, and AGENTS text back into the analysis window instead of only user-facing product work.

## 2026-07-08 Improvements

55. Prove Product Design capability before treating `$product-design` as available.
- Evidence: `$product-design` was requested, but the plugin state path was missing and tool discovery returned no Product Design analysis callable.
- Small change: service-analysis runs should report `productDesignContext`, `toolSurface`, `toolAvailable`, and `fallbackSource` before spending analysis budget.

56. Exclude self and approval-review sessions from conversation mining.
- Evidence: the current automation run and its approval-review subagent session appeared in the same `/Users/keelim/.codex/sessions/2026/07/*` search window being analyzed.
- Small change: session mining should filter `currentThreadId`, `parent_thread_id`, `source.subagent`, and approval-only transcripts before summarizing service improvements.

## 2026-07-09 Follow-Up Evidence

- Product Design context remains absent: `/Users/keelim/.codex/state/plugins/product-design/user-context.md` was not present.
- Since the previous project-management marker, six session files were newer than `2026-07-08T00:01:25Z`: the current automation thread, two guardian approval-review subagent threads, the prior project-management automation thread, and one user-facing Rich daily market snapshot automation thread.
- The Rich daily market snapshot session in `/Users/keelim/Desktop/keelim-maestro/rich` collected and verified `2026-07-07` and `2026-07-08` through `DailyMarketSnapshotStore().list_snapshot_dates()`, but the verified SQLite change still needed this project-management sweep to commit it.
- `tools/codex-hygiene/codex-hygiene.sh --dry-run` could not read the process table in sandbox, and escalated process inspection was denied by the approval reviewer; `tools/agentgateway/scripts/stop-k8s-gateway.sh --dry-run` still proved no matching Kubernetes port-forward.

## 2026-07-09 Improvements

57. Carry producer automation commit intent forward explicitly.
- Evidence: the Rich snapshot automation verified persisted dates `2026-07-07` and `2026-07-08`, while the SQLite file remained dirty until the next project-management run.
- Small change: producer automations that mutate repo state should report `changedFiles`, `verifyCommand`, `commitEligible`, and `suggestedCommitMessage`.

58. Add policy-aware process hygiene status.
- Evidence: process-table inspection was blocked first by sandbox, then by approval policy, while the safer agentgateway port-forward dry-run succeeded.
- Small change: process cleanup reports should split `scriptRan`, `sandboxBlocked`, `approvalDenied`, `safeFallbackChecked`, and `cleanupApplied`.

59. Prefer a session whitelist over broad conversation mining.
- Evidence: among six newer session files, only the Rich snapshot automation was user-facing product work; the rest were current/previous project-management or guardian approval-review transcripts.
- Small change: session analysis should whitelist `thread_source=automation` with non-self cwd/task evidence, then exclude guardian/subagent approval transcripts by default.

## 2026-07-11 Follow-Up Evidence

- Product Design-specific analysis tooling was still not exposed in this
  surface; discovery returned site-design picker / Creative Production widgets
  rather than a callable Product Design service-analysis tool.
- The thin Codex worktree again lacked `tools/`, while the hydrated checkout
  `/Users/keelim/Desktop/keelim-maestro` had the real child repo state and
  process-hygiene scripts.
- `tools/codex-hygiene/codex-hygiene.sh --dry-run` needed process-table access
  outside the sandbox and then reported no runaway native-hook scans,
  `node_repl=0`, and stdio app-server `count=0`; the agentgateway Kubernetes
  port-forward dry-run also found no matching process.
- `rich` contained pre-staged admin UI / SQLite / generated TypeScript state,
  plus a separate untracked infinite-buy calculator route. The calculator route
  was verified and committed as `d63dd97` using an explicit pathspec while the
  older staged work was left intact.
- A bare `bun test` run against `admin-navigation.test.tsx` failed with
  `ReferenceError: window is not defined`, while the package-local
  `bun run --cwd web test -- ...` command used `web/vitest.config.ts` and
  passed the same navigation plus calculator tests.
- Recent root commit scanning since the previous marker surfaced remote refs
  `e37e3d7` and `f64dbbc`; both passed `git show --check`. The `e37e3d7`
  branch touched `docs/idea/toto.md`, but the checked-out root tree still keeps
  `toto` archived in the idea index.

## 2026-07-11 Improvements

60. Label commit-scan scope before proposing a bug fix.
- Evidence: recent scanning found remote-only refs (`e37e3d7`, `f64dbbc`) as
well as the checked-out local branch, and the `toto` archive concern applied to
the remote branch diff rather than the current working tree.
- Small change: bug triage output should report `checkedOutBranch`,
`remoteOnlyRef`, `mergeCandidate`, and `currentTreeState` before asking the
operator to patch a recent commit.

61. Store package-local frontend test commands as proof surfaces.
- Evidence: bare `bun test web/src/...admin-navigation.test.tsx` failed because
`window` was unavailable, but `bun run --cwd web test -- src/...` loaded the
Vitest/jsdom config and passed 18 tests.
- Small change: Product Design and automation handoffs for frontend work should
record `cwd`, `packageScript`, `configFile`, `environment`, and `testedPaths`
instead of only the test filename.

62. Preserve mixed staging lanes during automated commits.
- Evidence: `rich` had older staged admin UI / SQLite / `tsconfig.tsbuildinfo`
state, while the infinite-buy calculator was a separate verified unit committed
as `d63dd97` with `git commit --only` pathspecs.
- Small change: commit automation should expose `preStagedFiles`,
`committedPathspecs`, `leftStagedFiles`, and `verificationCommands` per commit
so unrelated staged work is not silently swept in.

## 2026-07-12 Follow-Up Evidence

- Product Design-specific local context is still absent:
  `/Users/keelim/.codex/state/plugins/product-design` does not exist in this
  run.
- Root commit `c4ba509` added
  `docs/research/subproject-architecture-opportunities-2026-07-11.html`, a
  ranked architecture opportunity report with 9 proposals and an explicit root
  changeset manifest recommendation.
- Root commit `4668b4e` implemented the first root changeset manifest validator:
  `scripts/validate-changeset-manifest.mjs` is inspection-only, requires clean
  autonomous repo roots, full 40-character SHAs, simple required-check commands,
  unique contiguous order values, and rollback instructions. `bun run test`
  passed after the commit.
- Session mining since the previous marker found a high-signal user-facing
  YouTube audit session at
  `/Users/keelim/.codex/sessions/2026/07/11/rollout-2026-07-11T10-23-55-019f4ec6-21f4-7fe0-9677-5183072c2c23.jsonl`.
  It reported 13 public Shorts, last publish on 2026-06-28, a 13-day gap,
  recent 28-day views 582, engaged views 270, subscribers +1, continue/swipe
  split 45.6%/54.4%, and latest GPT-5.6 average viewed 24.9%.
- The same YouTube session concluded that the immediate need is publish-loop
  recovery, not another production tool: Microsoft Intelligent Terminal has
  local package/render assets but near-silent audio and unfinished human/critic
  gates, while the repo also has 172 tracked deletions and 35 untracked files.
- Recent-commit verification found no concrete new bug: `git show --check`
  passed for root commits `4668b4e` and `c4ba509`, child commits `aec806edb`,
  `c4d827a`, `d359046`, `6b4bb3a`, `c2f9d99`, `eb21049`, and new Rich commit
  `6f51d47`; targeted tests passed for the touched surfaces.
- The first `all` Gradle test attempt failed only because sandboxed access to
  `/Users/keelim/.gradle/.../gradle-9.3.1-bin.zip.lck` was not permitted; the
  exact escalated rerun of
  `./gradlew :feature:app-function:testDebugUnitTest --tests com.keelim.appfunction.json.JsonFormatterAppFunctionsTest`
  finished `BUILD SUCCESSFUL`.

## 2026-07-12 Improvements

63. Link opportunity reports to implementation and proof status.
- Evidence: `c4ba509` produced a 9-item architecture opportunity report, and
`4668b4e` implemented one of its root recommendations as a tested manifest
validator.
- Small change: Product Design/opportunity reports should carry `proposalId`,
`implementedCommit`, `verificationCommand`, and `status` fields so the next run
can distinguish new ideas from already-landed work.

64. Make cross-repo change planning preview-only by default.
- Evidence: `scripts/validate-changeset-manifest.mjs` validates repo roots,
clean trees, HEAD SHAs, command shapes, ordering, and rollback text, while its
header explicitly says it never checks out commits, runs checks, pushes, or
updates root pointers.
- Small change: service planning for child repos should first show a
read-only changeset manifest preview with repo, HEAD, required checks, order,
and rollback before offering any mutation.

65. Turn channel audits into publish-loop recovery cards.
- Evidence: the YouTube audit found a 13-day publishing gap, near-silent
Microsoft renders, unfinished human/critic gates, and a large uncommitted repo
batch, while explicitly saying new production tooling is not the bottleneck.
- Small change: content-product sessions should surface `lastPublishedAt`,
`gapDays`, `nextCandidate`, `blockingAsset`, `humanApprovalStatus`, and
`repoPreservationState` before proposing rendering features.

66. Separate sandbox permission failures from real test failures.
- Evidence: the `all` Gradle check first failed on a user-home `.gradle` lock
permission error, then the same test command passed outside the sandbox.
- Small change: verification ledgers should record `firstRunBlockedBySandbox`,
`rerunCommand`, and `rerunResult` so a passing rerun does not leave a false
project bug signal.
