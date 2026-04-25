# Agent Codemap

- Repository: `toto`
- Root: `/Users/keelim/Desktop/keelim-maestro/toto`
- Generated: 2026-04-25 04:52 UTC
- Files scanned: 28
- Detected shape: Node/JavaScript, Python

## Read First
- `README.md`
- `package.json`
- `pyproject.toml`
- `streamlit_app/app.py`

## Repository Shape
- Python: 18 files
- .txt: 4 files
- [no extension]: 2 files
- Markdown: 2 files
- .json: 1 files
- .toml: 1 files

## Entrypoints
- `streamlit_app/app.py`

## Key Directories
- `src/`: 13 files; examples: `src/kbo_dashboard/__init__.py`, `src/kbo_dashboard/bootstrap.py`, `src/kbo_dashboard/contracts.py`
- `streamlit_app/`: 5 files; examples: `streamlit_app/Home.py`, `streamlit_app/__init__.py`, `streamlit_app/app.py`
- `tests/`: 5 files; examples: `tests/test_dto_contracts.py`, `tests/test_empty_states.py`, `tests/test_filters_and_state.py`
- `./`: 4 files; examples: `.gitignore`, `README.md`, `package.json`
- `docs/`: 1 files; examples: `docs/2026-04-18-audit-report.md`

## Dependencies and Tooling
- `README.md`
- `package.json`
- `pyproject.toml`

## Useful Commands
- npm script `bootstrap`: python3 -m venv .venv && .venv/bin/python -m pip install --upgrade pip setuptools wheel && .venv/bin/python -m pip install -e '.[dev]'
- npm script `compile`: PYTHONPYCACHEPREFIX=/tmp/pycache-toto .venv/bin/python -m compileall src streamlit_app tests
- npm script `dev`: .venv/bin/python -m streamlit run streamlit_app/app.py
- npm script `seed`: .venv/bin/python -m kbo_dashboard.bootstrap --reset
- npm script `test`: .venv/bin/python -m pytest
- npm script `verify`: bun run test && bun run compile

## Tests and Verification
- `tests/test_dto_contracts.py`
- `tests/test_empty_states.py`
- `tests/test_filters_and_state.py`
- `tests/test_no_recommendation_surface.py`
- `tests/test_repository.py`

## Symbol Landmarks
- `src/kbo_dashboard/bootstrap.py`: project_root (L9), default_db_path (L13), get_repository (L17), main (L24)
- `src/kbo_dashboard/contracts.py`: _clamp (L7), normalize_triplet (L11), DashboardFilters (L23), normalized_team (L27), normalized_confidence (L32), PredictionCardDTO (L37), __post_init__ (L53), BacktestSummaryDTO (L67)
- `src/kbo_dashboard/repository.py`: DashboardRepository (L18), __init__ (L19), _connect (L24), _ensure_schema (L29), has_seed_data (L82), seed_demo_data (L87), get_today_cards (L271), get_model_summaries (L295)
- `src/kbo_dashboard/streamlit_support.py`: configure_page (L32), render_base_styles (L37), prepare_page (L87), render_sidebar (L100), render_header (L129), render_summary_cards (L152), render_empty_state (L164), render_probability_bar (L176)
- `src/kbo_dashboard/ui/state.py`: ensure_session_defaults (L19), filters_from_state (L24), available_team_options (L32)
- `src/kbo_dashboard/ui/view_models.py`: SummaryMetric (L11), EmptyState (L18), build_summary_metrics (L24), resolve_today_empty_state (L42), resolve_model_empty_state (L64), resolve_mapping_empty_state (L71), selected_model_name (L79), selection_rationale (L87)
- `tests/test_dto_contracts.py`: test_prediction_card_normalizes_probabilities (L8), test_prediction_card_fields_are_complete (L31)
- `tests/test_empty_states.py`: test_today_empty_state_for_no_games (L13), test_model_empty_state_for_missing_backtest (L28), test_mapping_empty_state_for_missing_rows (L34), test_future_date_without_cards_is_true_no_games (L49), test_cancelled_games_take_priority_for_today (L64), test_non_today_filtered_empty_is_not_no_games (L79)
- `tests/test_filters_and_state.py`: test_session_defaults_are_applied (L6), test_filters_from_state_normalizes_all_teams (L15)
- `tests/test_no_recommendation_surface.py`: test_app_source_avoids_forbidden_surface_terms (L6)
- `tests/test_repository.py`: test_seed_data_populates_all_sections (L9), test_filters_affect_visible_cards (L24), test_date_filter_returns_tomorrow_row_and_empty_future_date (L37)

## Open Questions
- No existing `docs/CODEMAPS/*` files were found.
- No root `AGENTS.md` was found; check for deeper instruction files before editing.
