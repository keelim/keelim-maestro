#!/bin/sh
set -eu

print_usage() {
  cat <<'EOF'
Usage:
  scripts/verify-all-web-ui-integration.sh [--full]

Checks the cross-repo all-web-ui integration contract from the workspace root.

Default mode:
  - static contract checks only

--full:
  - static contract checks
  - runtime verification commands for all-web-ui, rich/web, keelim-vercel
EOF
}

FULL_MODE="0"

case "${1:-}" in
  "")
    ;;
  --full)
    FULL_MODE="1"
    ;;
  -h|--help)
    print_usage
    exit 0
    ;;
  *)
    print_usage
    exit 1
    ;;
esac

CURRENT_ROOT="$(git rev-parse --show-toplevel)"

resolve_workspace_root() {
  if [ -n "${OMX_TEAM_STATE_ROOT:-}" ] && [ -d "${OMX_TEAM_STATE_ROOT%/}" ]; then
    cd "${OMX_TEAM_STATE_ROOT%/}/../.." && pwd
    return 0
  fi

  if [ -d "$CURRENT_ROOT/rich/.git" ] && [ -d "$CURRENT_ROOT/keelim-vercel/.git" ]; then
    printf '%s\n' "$CURRENT_ROOT"
    return 0
  fi

  printf '%s\n' "$CURRENT_ROOT"
}

WORKSPACE_ROOT="$(resolve_workspace_root)"
ALL_WEB_UI_DIR="$WORKSPACE_ROOT/all-web-ui"
RICH_WEB_DIR="$WORKSPACE_ROOT/rich/web"
KEELIM_VERCEL_DIR="$WORKSPACE_ROOT/keelim-vercel"

FAILURES=0

pass() {
  printf 'PASS  %s\n' "$1"
}

fail() {
  printf 'FAIL  %s\n' "$1"
  FAILURES=$((FAILURES + 1))
}

run_check() {
  description="$1"
  shift

  if "$@"; then
    pass "$description"
  else
    fail "$description"
  fi
}

path_is_git_repo() {
  target="$1"
  [ -d "$target/.git" ] || [ -f "$target/.git" ]
}

package_has_dependency() {
  package_json="$1"
  dependency_name="$2"

  jq -e --arg dependency_name "$dependency_name" '
    (.dependencies // {})[$dependency_name]
    // (.devDependencies // {})[$dependency_name]
    // (.peerDependencies // {})[$dependency_name]
  ' "$package_json" >/dev/null
}

package_script_exists() {
  package_json="$1"
  script_name="$2"

  jq -e --arg script_name "$script_name" '(.scripts // {})[$script_name]' "$package_json" >/dev/null
}

git_has_remote() {
  repo_dir="$1"
  remote_name="$2"

  git -C "$repo_dir" remote get-url "$remote_name" >/dev/null 2>&1
}

branch_is_main() {
  repo_dir="$1"
  current_branch="$(git -C "$repo_dir" symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
  [ "$current_branch" = "main" ]
}

file_contains() {
  file_path="$1"
  pattern="$2"

  rg -q --fixed-strings "$pattern" "$file_path"
}

update_subrepos_status_lists_repo() {
  repo_path="$1"

  "$WORKSPACE_ROOT/scripts/update-subrepos.sh" status | rg -q "^${repo_path}[[:space:]]+branch="
}

all_web_ui_has_style_entrypoints() {
  (
    cd "$ALL_WEB_UI_DIR" &&
      {
        [ -f "src/styles/styles.css" ] || [ -f "src/styles/tokens.css" ];
      } &&
      {
        [ -f "src/styles/themes/finance.css" ] || [ -f "src/styles/theme-finance.css" ];
      } &&
      {
        [ -f "src/styles/themes/admin-bw.css" ] || [ -f "src/styles/theme-admin-bw.css" ];
      }
  )
}

directory_has_minimum_files() {
  directory="$1"
  minimum="$2"
  shift 2

  count=0
  for name in "$@"; do
    if [ -f "$directory/$name" ]; then
      count=$((count + 1))
    fi
  done

  [ "$count" -ge "$minimum" ]
}

imports_all_web_ui_anywhere() {
  target_dir="$1"
  rg -q "(from|import) ['\"][^'\"]*all-web-ui" "$target_dir"
}

keelim_boundary_imports_valid() {
  if ! imports_all_web_ui_anywhere "$KEELIM_VERCEL_DIR"; then
    return 0
  fi

  invalid_imports="$(
    cd "$KEELIM_VERCEL_DIR" &&
      rg -n "from ['\"]all-web-ui" app components lib \
        -g '!components/ui/**' \
        -g '!components/shared/**' \
        -g '!lib/ui-adapters/**' || true
  )"

  [ -z "$invalid_imports" ]
}

keelim_components_ui_is_clean() {
  if [ ! -d "$KEELIM_VERCEL_DIR/components/ui" ]; then
    return 0
  fi

  ! rg -q "from ['\"]all-web-ui" "$KEELIM_VERCEL_DIR/components/ui"
}

print_header() {
  printf 'Workspace root: %s\n' "$WORKSPACE_ROOT"
  printf 'Mode: %s\n\n' "$( [ "$FULL_MODE" = "1" ] && printf 'full' || printf 'static' )"
}

run_static_checks() {
  run_check "all-web-ui repo exists" path_is_git_repo "$ALL_WEB_UI_DIR"
  run_check "rich/web repo exists" path_is_git_repo "$WORKSPACE_ROOT/rich"
  run_check "keelim-vercel repo exists" path_is_git_repo "$KEELIM_VERCEL_DIR"
  run_check "all-web-ui has origin remote" git_has_remote "$ALL_WEB_UI_DIR" "origin"
  run_check "root .gitignore excludes all-web-ui" file_contains "$WORKSPACE_ROOT/.gitignore" "/all-web-ui/"
  run_check "update-subrepos status lists all-web-ui" update_subrepos_status_lists_repo "all-web-ui"

  if path_is_git_repo "$ALL_WEB_UI_DIR"; then
    run_check "all-web-ui default branch is main" branch_is_main "$ALL_WEB_UI_DIR"
    run_check "all-web-ui has package.json" test -f "$ALL_WEB_UI_DIR/package.json"
    run_check "all-web-ui has typecheck script" package_script_exists "$ALL_WEB_UI_DIR/package.json" "typecheck"
    run_check "all-web-ui has test script" package_script_exists "$ALL_WEB_UI_DIR/package.json" "test"
    run_check \
      "all-web-ui exports core primitive source files" \
      directory_has_minimum_files \
      "$ALL_WEB_UI_DIR/src/components" \
      5 \
      "button.tsx" "input.tsx" "panel.tsx" "card.tsx" "badge.tsx" "loading-status.tsx" "empty-state.tsx"
    run_check \
      "all-web-ui defines shared style entrypoints" \
      all_web_ui_has_style_entrypoints
  fi

  if [ -f "$RICH_WEB_DIR/package.json" ]; then
    run_check "rich/web depends on all-web-ui" package_has_dependency "$RICH_WEB_DIR/package.json" "all-web-ui"
    run_check "rich/web imports all-web-ui somewhere under src" imports_all_web_ui_anywhere "$RICH_WEB_DIR/src"
  else
    fail "rich/web package.json exists"
  fi

  run_check \
    "rich admin layout still applies admin-bw-theme" \
    file_contains \
    "$RICH_WEB_DIR/src/app/admin/layout.tsx" \
    "admin-bw-theme"
  run_check \
    "rich root layout still renders AgentationToolbar" \
    file_contains \
    "$RICH_WEB_DIR/src/app/layout.tsx" \
    "AgentationToolbar"

  if [ -f "$KEELIM_VERCEL_DIR/package.json" ]; then
    run_check "keelim-vercel depends on all-web-ui" package_has_dependency "$KEELIM_VERCEL_DIR/package.json" "all-web-ui"
  else
    fail "keelim-vercel package.json exists"
  fi

  run_check "keelim-vercel keeps components/ui free of all-web-ui imports" keelim_components_ui_is_clean
  run_check "keelim-vercel all-web-ui imports stay in adapter-safe locations" keelim_boundary_imports_valid
}

run_command_check() {
  label="$1"
  shift

  printf '\n[cmd] %s\n' "$label"
  if "$@"; then
    pass "$label"
  else
    fail "$label"
  fi
}

run_with_lock_retry() {
  retry_pattern="$1"
  shift

  output_file="$(mktemp)"
  if "$@" >"$output_file" 2>&1; then
    cat "$output_file"
    rm -f "$output_file"
    return 0
  fi

  cat "$output_file"
  if rg -q --fixed-strings "$retry_pattern" "$output_file"; then
    printf '[retry] matched lock pattern, retrying once...\n'
    sleep 1
    if "$@" >"$output_file" 2>&1; then
      cat "$output_file"
      rm -f "$output_file"
      return 0
    fi
    cat "$output_file"
  fi

  rm -f "$output_file"
  return 1
}

run_full_checks() {
  run_command_check "all-web-ui typecheck" sh -c "cd \"$ALL_WEB_UI_DIR\" && bun run typecheck"
  run_command_check "all-web-ui test" sh -c "cd \"$ALL_WEB_UI_DIR\" && bun test"
  run_command_check "rich/web typecheck" sh -c "cd \"$RICH_WEB_DIR\" && bun run typecheck"
  run_command_check "rich/web test" sh -c "cd \"$RICH_WEB_DIR\" && bun run test"
  run_command_check "rich/web build" sh -c "cd \"$RICH_WEB_DIR\" && bun run build"
  run_command_check "keelim-vercel typecheck" sh -c "cd \"$KEELIM_VERCEL_DIR\" && bun run typecheck"
  run_command_check "keelim-vercel lint" sh -c "cd \"$KEELIM_VERCEL_DIR\" && bun run lint"
  run_command_check \
    "keelim-vercel build" \
    run_with_lock_retry \
    "Unable to acquire lock" \
    sh -c "cd \"$KEELIM_VERCEL_DIR\" && bun run build"
}

print_header
run_static_checks

if [ "$FULL_MODE" = "1" ] && [ "$FAILURES" -eq 0 ]; then
  run_full_checks
fi

printf '\n'
if [ "$FAILURES" -eq 0 ]; then
  printf 'Integration verification passed.\n'
else
  printf 'Integration verification failed (%s issue%s).\n' "$FAILURES" "$( [ "$FAILURES" -eq 1 ] && printf '' || printf 's' )"
fi

exit "$FAILURES"
