# Agent Codemap

- Repository: `keelim-plugin`
- Root: `/home/user/keelim-maestro/keelim-plugin`
- Generated: 2026-08-11 00:11 UTC
- Files scanned: 30
- Detected shape: Source repository

## Read First
- `README.md`

## Repository Shape
- Python: 11 files
- Markdown: 10 files
- YAML: 6 files
- [no extension]: 1 files
- HTML: 1 files
- Shell: 1 files

## Entrypoints
- No obvious entrypoint files detected.

## Key Directories
- `skills/`: 28 files; examples: `skills/codebase-codemap/SKILL.md`, `skills/codebase-codemap/agents/openai.yaml`, `skills/codebase-codemap/references/codemap-schema.md`
- `./`: 2 files; examples: `.gitignore`, `README.md`

## Dependencies and Tooling
- `README.md`

## Useful Commands
- No package or pyproject scripts detected. Inspect README or project docs for commands.

## Tests and Verification
- No obvious test files detected.

## Symbol Landmarks
- `skills/codebase-codemap/scripts/generate_codemap.py`: relpath (L203), should_skip_dir (L207), is_probably_binary (L214), iter_repo_files (L224), read_text (L240), project_filename (L248), classify_repo (L254), collect_manifests (L273)
- `skills/jira-ticket-desk/scripts/render_ticket_desk.py`: load_json (L42), write_json (L47), pick (L52), strip_remote_urls (L60), nested_name (L70), extract_issues (L78), normalize_issue (L91), load_rules (L118)
- `skills/jira-ticket-desk/scripts/test_render_ticket_desk.py`: test_demo_html_is_offline (L18), test_local_rules_override_bucket_and_reason (L26), test_remote_urls_are_omitted_from_display_text (L51), test_data_json_can_be_swapped_into_template (L68), main (L79)
- `skills/session-learning/scripts/install_hooks.py`: HookTarget (L32), utc_stamp (L37), run_git (L41), detect_project_root (L58), project_id (L66), skill_root_from_script (L72), default_codex_hooks_path (L76), default_claude_hooks_path (L80)
- `skills/session-learning/scripts/learning_observer.py`: utc_now (L33), slug_timestamp (L37), scrub (L41), load_payload (L52), first_present (L64), run_git (L71), root_from_cwd (L88), detect_project_root (L100)
- `skills/session-learning/scripts/review_candidates.py`: Candidate (L31), Recommendation (L38), parse_frontmatter (L45), read_candidate (L60), candidate_files (L66), text_for_classification (L77), classify (L89), recommend (L111)
- `skills/session-learning/scripts/test_install_hooks.py`: run_installer (L18), load (L39), session_entries (L43), InstallHooksTests (L51), test_dry_run_does_not_write_configs (L52), test_apply_adds_codex_and_claude_hooks (L63), test_global_scope_omits_project_scope_root (L78), test_apply_is_idempotent (L91)
- `skills/session-learning/scripts/test_learning_observer.py`: LearningObserverTests (L18), run_observer (L19), test_redacts_secrets (L39), test_malformed_json_writes_parse_error (L56), test_stop_writes_candidate (L64), test_scope_root_skips_outside_project (L78)
- `skills/session-learning/scripts/test_review_candidates.py`: write_candidate (L17), run_review (L26), ReviewCandidatesTests (L38), test_routes_candidates_by_promotion_scope (L39), test_honors_explicit_non_project_scope (L55)
- `skills/session-usage-dashboard/scripts/build_session_usage_dashboard.py`: utc_now (L43), timestamp_slug (L47), safe_text (L51), read_jsonl (L60), h (L76), UsageCollector (L80), __init__ (L81), add_input (L92)
- `skills/session-usage-dashboard/scripts/test_build_session_usage_dashboard.py`: write_jsonl (L19), test_codex_and_claude_counts_and_offline_outputs (L23), test_missing_inputs_warn_without_crashing (L112)

## Open Questions
- Verification surface is unclear; inspect README, CI, or manifests before changing behavior.
- No existing `docs/CODEMAPS/*` files were found.
- No root `AGENTS.md` was found; check for deeper instruction files before editing.
- Entrypoints were not obvious from file names; inspect manifests and top-level directories.
