# Agent Codemap

- Repository: `keelim-plugin`
- Root: `/home/user/keelim-maestro/keelim-plugin`
- Generated: 2026-10-08 00:20 UTC
- Files scanned: 85
- Detected shape: Python

## Read First
- `AGENTS.md`
- `README.md`
- `pyproject.toml`

## Repository Shape
- Python: 33 files
- Markdown: 22 files
- YAML: 15 files
- .sample: 3 files
- Shell: 3 files
- .lock: 2 files
- .toml: 2 files
- HTML: 2 files
- [no extension]: 1 files
- .json: 1 files
- JavaScript: 1 files

## Entrypoints
- No obvious entrypoint files detected.

## Key Directories
- `skills/`: 43 files; examples: `skills/agent-instructions-improver/SKILL.md`, `skills/agent-instructions-improver/agents/openai.yaml`, `skills/agent-instructions-improver/references/quality-criteria.md`
- `evals/`: 22 files; examples: `evals/skillopt/agent-instructions-improver/README.md`, `evals/skillopt/agent-instructions-improver/configs/_base_/default.yaml`, `evals/skillopt/agent-instructions-improver/configs/agent_instructions_improver/codex_only.yaml`
- `./`: 10 files; examples: `.gitignore`, `.pre-commit-config.yaml`, `AGENTS.md`
- `scripts/`: 9 files; examples: `scripts/check.sh`, `scripts/gen-catalog.mjs`, `scripts/promote_plugin_skills.py`
- `.github/`: 1 files; examples: `.github/workflows/ci.yml`

## Dependencies and Tooling
- `.github/workflows/ci.yml`
- `AGENTS.md`
- `README.md`
- `evals/skillopt/agent-instructions-improver/README.md`
- `evals/skillopt/plugin-skill-improver/README.md`
- `pyproject.toml`
- `uv.lock`

## Useful Commands
- No package or pyproject scripts detected. Inspect README or project docs for commands.

## Tests and Verification
- No obvious test files detected.

## Symbol Landmarks
- `evals/skillopt/test_eval_configs.py`: scalar_value (L16), nested_int (L23), EvalConfigTests (L34), test_codex_configs_have_resolvable_base_and_holdout_counts (L35), test_score_fixture_samples_cover_multiple_cases (L46)
- `evals/skillopt/test_eval_overlays.py`: load_module (L21), DataloaderTests (L53), assert_loader_formats (L54), test_plugin_loader_supports_json_jsonl_and_wrappers (L78), test_agent_loader_supports_json_jsonl_and_wrappers (L81), EvaluatorTests (L85), assert_substring_scoring (L86), test_plugin_evaluator_substring_scoring (L107)
- `evals/skillopt/agent-instructions-improver/overlays/skillopt/envs/agent_instructions_improver/adapter.py`: AgentInstructionsImproverAdapter (L22), __init__ (L27), setup (L65), get_dataloader (L69), build_env_from_batch (L72), build_train_env (L76), build_eval_env (L80), rollout (L84)
- `evals/skillopt/agent-instructions-improver/overlays/skillopt/envs/agent_instructions_improver/dataloader.py`: SplitDataLoader (L12), load_raw_items (L13), load_items (L17), AgentInstructionsImproverDataLoader (L35), load_raw_items (L38)
- `evals/skillopt/agent-instructions-improver/overlays/skillopt/envs/agent_instructions_improver/evaluator.py`: normalize_text (L9), _contains (L13), evaluate (L17)
- `evals/skillopt/agent-instructions-improver/overlays/skillopt/envs/agent_instructions_improver/rollout.py`: _item_text (L26), build_user_prompt (L30), build_system_prompt (L55), _build_codex_skill (L65), _run_codex_target (L78), process_one (L106), run_batch (L185), _timeout_result (L219)
- `evals/skillopt/agent-instructions-improver/overlays/skillopt/model/codex_chat_backend.py`: CompatAssistantMessage (L31), model_dump (L38), _bool_env (L43), _int_env (L50), _output_root (L60), _new_run_dir (L64), _messages_to_prompt (L80), _build_exec_prompt (L91)
- `evals/skillopt/plugin-skill-improver/overlays/skillopt/envs/plugin_skill_improver/adapter.py`: PluginSkillImproverAdapter (L20), __init__ (L25), setup (L63), get_dataloader (L67), build_env_from_batch (L70), build_train_env (L74), build_eval_env (L78), rollout (L82)
- `evals/skillopt/plugin-skill-improver/overlays/skillopt/envs/plugin_skill_improver/dataloader.py`: SplitDataLoader (L12), load_raw_items (L13), load_items (L17), PluginSkillImproverDataLoader (L35), load_raw_items (L38)
- `evals/skillopt/plugin-skill-improver/overlays/skillopt/envs/plugin_skill_improver/evaluator.py`: normalize_text (L9), _contains (L13), evaluate (L17)
- `evals/skillopt/plugin-skill-improver/overlays/skillopt/envs/plugin_skill_improver/rollout.py`: _item_text (L26), build_user_prompt (L30), build_system_prompt (L62), _build_codex_skill (L72), _run_codex_target (L85), process_one (L113), run_batch (L192), _timeout_result (L226)
- `scripts/promote_plugin_skills.py`: Skill (L32), PromotionResult (L38), as_json (L46), skill_dirs (L57), select_skills (L69), split_frontmatter (L80), frontmatter_values (L88), preserve_current_frontmatter (L97)
- `scripts/run-tests.py`: run (L14), unique (L20), python_files (L24), test_files (L34), main (L44)
- `scripts/skillopt_agent_instructions.py`: eprint (L65), run (L69), uv_python_cmd (L95), normalize_text (L108), score_response (L112), default_examples (L132), observations_paths (L243), keywords_from_text (L252)
- `scripts/skillopt_plugin_skills.py`: SkillInfo (L77), GateResult (L86), as_json (L92), eprint (L101), default_subprocess_timeout (L105), run (L116), uv_python_cmd (L152), uv_python_with_cmd (L165)
- `scripts/test_security_guards.py`: load_module (L18), PromoteSecurityTests (L35), test_explicit_candidate_must_stay_under_candidate_root_by_default (L36), test_stage_root_must_stay_under_promote_candidates_by_default (L51), SkillOptSecurityTests (L58), test_agent_runner_env_uses_allowlist_and_scrubs_model_provider_keys (L59), test_custom_codex_exec_requires_trust_env (L79), test_plugin_runner_verifies_pinned_skillopt_revision (L89)
- `scripts/verify_skills.py`: parse_scalar (L25), parse_simple_yaml (L40), parse_yaml (L70), split_frontmatter (L81), readme_skill_names (L90), validate_codex_meta (L101), validate_capabilities (L128), extract_backticked_bullets (L154)
- `skills/codebase-codemap/scripts/generate_codemap.py`: relpath (L203), should_skip_dir (L207), is_probably_binary (L214), is_within (L224), default_allowed_scan_root (L232), resolve_repo_root (L252), resolve_output_path (L267), iter_repo_files (L280)
- `skills/codebase-codemap/scripts/test_generate_codemap.py`: write (L13), GenerateCodemapTests (L18), test_generate_markdown_finds_manifests_tests_and_symbols (L19), test_iter_repo_files_skips_private_hidden_and_dependency_dirs (L40), test_default_output_writes_project_named_codemap (L61), test_output_dir_writes_project_named_codemap (L76), test_outside_repo_scan_requires_explicit_flag (L86), test_absolute_output_requires_explicit_flag (L93)
- `skills/codex-insights/scripts/insight_observer.py`: UnsafeStoragePath (L45), insight_env (L49), utc_now (L54), slug_timestamp (L58), stable_identifier (L62), cwd_category (L70), load_payload (L80), first_present (L92)
- `skills/codex-insights/scripts/install_hooks.py`: HookTarget (L37), utc_stamp (L42), create_backup (L46), run_git (L67), detect_project_root (L84), project_id (L92), skill_root_from_script (L98), default_codex_hooks_path (L102)
- `skills/codex-insights/scripts/review_candidates.py`: Candidate (L31), Recommendation (L38), parse_frontmatter (L45), read_candidate (L60), candidate_files (L66), text_for_classification (L77), classify (L89), recommend (L156)
- `skills/codex-insights/scripts/test_insight_observer.py`: InsightObserverTests (L24), assert_policy_failure (L25), run_observer (L29), init_git (L49), add_gitlink (L59), test_never_persists_free_form_payload_content (L84), test_malformed_json_writes_parse_error (L120), test_stop_writes_candidate (L128)
- `skills/codex-insights/scripts/test_install_hooks.py`: run_installer (L19), load (L43), insight_entries (L47), InstallHooksTests (L55), test_dry_run_does_not_write_configs (L56), test_apply_adds_codex_and_claude_hooks (L67), test_custom_hook_path_requires_explicit_allow_flag (L82), test_external_skill_root_requires_trust_flag (L108)
- `skills/codex-insights/scripts/test_review_candidates.py`: write_candidate (L17), run_review (L26), run_review_markdown (L38), ReviewCandidatesTests (L50), test_routes_candidates_by_promotion_scope (L51), test_honors_explicit_non_project_scope (L77), test_since_days_filters_old_candidates (L90), test_empty_results_render_json_and_markdown (L103)
- `skills/html-report-generator/scripts/render_html_report.py`: load_json (L159), is_within (L167), resolve_output_path (L175), clean_text (L189), h (L195), list_of_mappings (L199), list_of_values (L205), render_paragraphs (L211)
- `skills/html-report-generator/scripts/test_render_html_report.py`: test_demo_report_renders_and_validates (L21), test_rendering_escapes_text_and_omits_remote_urls (L32), test_validator_rejects_remote_assets_and_network_apis (L46), test_cli_check_html_fails_for_unsafe_file (L69), test_validate_failure_does_not_write_output (L77), test_output_outside_input_dir_requires_explicit_flag (L97), main (L112)
- `skills/jira-ticket-desk/scripts/render_ticket_desk.py`: load_json (L50), is_within (L55), resolve_output_path (L63), write_json (L77), pick (L82), strip_remote_urls (L90), nested_name (L100), extract_issues (L108)
- `skills/jira-ticket-desk/scripts/test_render_ticket_desk.py`: test_demo_html_is_offline (L19), test_local_rules_override_bucket_and_reason (L27), test_unknown_rule_bucket_falls_back_to_next (L52), test_remote_urls_are_omitted_from_display_text (L68), test_offline_check_rejects_link_with_intervening_attributes (L85), test_data_json_can_be_swapped_into_template (L91), test_output_outside_input_dir_requires_explicit_flag (L102), main (L116)
- `skills/session-usage-dashboard/scripts/build_session_usage_dashboard.py`: utc_now (L50), timestamp_slug (L54), safe_text (L58), redact_value (L72), display_path (L86), is_within (L99), resolve_output_dir (L107), read_jsonl (L123)
- `skills/session-usage-dashboard/scripts/test_build_session_usage_dashboard.py`: write_jsonl (L19), test_codex_and_claude_counts_and_offline_outputs (L23), test_missing_inputs_warn_without_crashing (L112), test_authorization_header_token_is_redacted (L119), test_json_key_and_long_token_values_are_redacted (L126), test_display_path_avoids_absolute_home_path (L133), test_find_current_codex_respects_scan_limit (L143), test_output_dir_must_stay_under_session_usage_without_override (L164)

## Open Questions
- Verification surface is unclear; inspect README, CI, or manifests before changing behavior.
- No existing `docs/CODEMAPS/*` files were found.
- Entrypoints were not obvious from file names; inspect manifests and top-level directories.
