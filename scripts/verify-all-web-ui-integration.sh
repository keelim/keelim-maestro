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

package_dependency_spec() {
  package_json="$1"
  dependency_name="$2"

  jq -r --arg dependency_name "$dependency_name" '
    (.dependencies // {})[$dependency_name]
    // (.devDependencies // {})[$dependency_name]
    // (.peerDependencies // {})[$dependency_name]
    // empty
  ' "$package_json"
}

root_workspace_includes() {
  workspace_path="$1"

  jq -e --arg workspace_path "$workspace_path" '
    (.workspaces // []) | index($workspace_path)
  ' "$WORKSPACE_ROOT/package.json" >/dev/null
}

consumer_lock_section() {
  workspace_path="$1"

  awk -v workspace_path="$workspace_path" '
    $0 == "    \"" workspace_path "\": {" {
      in_section = 1
    }

    in_section {
      print
    }

    in_section && $0 == "    }," {
      exit
    }
  ' "$WORKSPACE_ROOT/bun.lock"
}

consumer_lock_entry_matches() {
  workspace_path="$1"
  expected_spec="$2"

  consumer_lock_section "$workspace_path" |
    rg -q --fixed-strings "\"all-web-ui\": \"$expected_spec\""
}

consumer_lock_section_lacks() {
  workspace_path="$1"
  unexpected_spec="$2"

  ! consumer_lock_section "$workspace_path" |
    rg -q --fixed-strings "\"all-web-ui\": \"$unexpected_spec\""
}

all_web_ui_dependency_protocol_is_lockfile_coherent() {
  [ -f "$WORKSPACE_ROOT/package.json" ] || return 1
  [ -f "$WORKSPACE_ROOT/bun.lock" ] || return 1
  [ -f "$RICH_WEB_DIR/package.json" ] || return 1
  [ -f "$KEELIM_VERCEL_DIR/package.json" ] || return 1

  root_workspace_includes "all-web-ui" || return 1
  root_workspace_includes "rich/web" || return 1
  root_workspace_includes "keelim-vercel" || return 1

  rich_spec="$(package_dependency_spec "$RICH_WEB_DIR/package.json" "all-web-ui")"
  keelim_spec="$(package_dependency_spec "$KEELIM_VERCEL_DIR/package.json" "all-web-ui")"

  if [ "$rich_spec" = "file:../../all-web-ui" ] && [ "$keelim_spec" = "file:../all-web-ui" ]; then
    consumer_lock_entry_matches "rich/web" "file:../../all-web-ui" &&
      consumer_lock_entry_matches "keelim-vercel" "file:../all-web-ui" &&
      consumer_lock_section_lacks "rich/web" "workspace:*" &&
      consumer_lock_section_lacks "keelim-vercel" "workspace:*"
    return
  fi

  if [ "$rich_spec" = "workspace:*" ] && [ "$keelim_spec" = "workspace:*" ]; then
    consumer_lock_entry_matches "rich/web" "workspace:*" &&
      consumer_lock_entry_matches "keelim-vercel" "workspace:*" &&
      consumer_lock_section_lacks "rich/web" "file:../../all-web-ui" &&
      consumer_lock_section_lacks "keelim-vercel" "file:../all-web-ui"
    return
  fi

  return 1
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

all_web_ui_manifest_lists_exports() {
  manifest="$ALL_WEB_UI_DIR/src/manifest.ts"
  package_json="$ALL_WEB_UI_DIR/package.json"

  [ -f "$manifest" ] || return 1

  for export_path in \
    all-web-ui/accordion \
    all-web-ui/alert \
    all-web-ui/alert-dialog \
    all-web-ui/avatar \
    all-web-ui/button \
    all-web-ui/calendar \
    all-web-ui/card \
    all-web-ui/checkbox \
    all-web-ui/dialog \
    all-web-ui/badge \
    all-web-ui/hover-card \
    all-web-ui/input \
    all-web-ui/label \
    all-web-ui/popover \
    all-web-ui/progress \
    all-web-ui/radio-group \
    all-web-ui/scroll-area \
    all-web-ui/select \
    all-web-ui/skeleton \
    all-web-ui/slider \
    all-web-ui/switch \
    all-web-ui/table \
    all-web-ui/tabs \
    all-web-ui/textarea \
    all-web-ui/tooltip \
    all-web-ui/toast \
    all-web-ui/sheet \
    all-web-ui/dropdown-menu \
    all-web-ui/breadcrumb
  do
    rg -q --fixed-strings "exportPath: '$export_path'" "$manifest" || return 1
  done

  for subpath in \
    ./accordion \
    ./alert \
    ./alert-dialog \
    ./avatar \
    ./button \
    ./calendar \
    ./card \
    ./checkbox \
    ./dialog \
    ./badge \
    ./hover-card \
    ./input \
    ./label \
    ./popover \
    ./progress \
    ./radio-group \
    ./scroll-area \
    ./select \
    ./table \
    ./tabs \
    ./skeleton \
    ./slider \
    ./switch \
    ./textarea \
    ./tooltip \
    ./toast \
    ./sheet \
    ./dropdown-menu \
    ./breadcrumb \
    ./manifest
  do
    jq -e --arg subpath "$subpath" '.exports[$subpath]' "$package_json" >/dev/null || return 1
  done
}

keelim_components_ui_is_shim_only() {
  if [ ! -d "$KEELIM_VERCEL_DIR/components/ui" ]; then
    return 0
  fi

  (
    cd "$KEELIM_VERCEL_DIR" &&
      for file in components/ui/*.tsx; do
        [ -f "$file" ] || continue

        case "$file" in
          components/ui/flip-counter.tsx|components/ui/product-csv-manager.tsx|components/ui/theme-switch.tsx|components/ui/timer.tsx|components/ui/toaster.tsx)
            continue
            ;;
        esac

        rg -q "from ['\"]all-web-ui/" "$file" || return 1
        ! rg -q "cva\\(|@radix-ui/react-|className=\\{cn\\(|const .*Variants|kui-" "$file" || return 1
      done
  )
}

rich_web_has_no_legacy_color_tokens() {
  ! rg -q -- '--color-' "$RICH_WEB_DIR/src"
}

rich_web_generic_drift_is_allowlisted() {
  allowlist="$WORKSPACE_ROOT/scripts/all-web-ui-rich-allowed-drift.txt"
  [ -f "$allowlist" ] || return 1

  drift_files="$(
    cd "$WORKSPACE_ROOT" &&
      rg -l "from ['\"]@radix-ui/react-|cva\\(|const .*(_BUTTON_CLASS|_INPUT_CLASS|_PANEL_CLASS|_CARD_CLASS|_TABLE_|TEXTAREA_CLASS|CONTROL_BUTTON_CLASS|SUMMARY_CARD_CLASS|SECTION_CARD_CLASS)" rich/web/src \
        -g '*.tsx' \
        -g '*.ts' | sort || true
  )"

  allowlisted_files="$(
    cd "$WORKSPACE_ROOT" &&
      rg -v '^[[:space:]]*(#|$)' "$allowlist" | sort || true
  )"

  [ "$drift_files" = "$allowlisted_files" ]
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
      10 \
      "button.tsx" "input.tsx" "panel.tsx" "card.tsx" "badge.tsx" "loading-status.tsx" "empty-state.tsx" "table.tsx" "tabs.tsx" "tooltip.tsx" "sheet.tsx" "dropdown-menu.tsx" "breadcrumb.tsx"
    run_check \
      "all-web-ui defines shared style entrypoints" \
      all_web_ui_has_style_entrypoints
    run_check \
      "all-web-ui manifest lists package exports" \
      all_web_ui_manifest_lists_exports
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

  run_check "all-web-ui dependency protocol is explicit and lockfile-coherent" all_web_ui_dependency_protocol_is_lockfile_coherent
  run_check "keelim-vercel components/ui is shim-only for generic primitives" keelim_components_ui_is_shim_only
  run_check "keelim-vercel all-web-ui imports stay in adapter-safe locations" keelim_boundary_imports_valid
  run_check "rich/web uses --kui-* token contract instead of legacy --color-* tokens" rich_web_has_no_legacy_color_tokens
  run_check "rich/web generic primitive drift is explicitly allowlisted" rich_web_generic_drift_is_allowlisted
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

run_optional_command_check() {
  label="$1"
  guard="$2"
  shift 2

  printf '\n[cmd] %s\n' "$label"
  if [ ! -e "$guard" ]; then
    printf 'SKIP  %s (missing %s)\n' "$label" "$guard"
    return 0
  fi

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
  run_command_check "root frozen Bun workspace install" sh -c "mkdir -p /tmp/keelim-maestro-bun-tmp && cd \"$WORKSPACE_ROOT\" && TMPDIR=/tmp/keelim-maestro-bun-tmp bun install --frozen-lockfile"
  run_command_check "all-web-ui typecheck" sh -c "cd \"$ALL_WEB_UI_DIR\" && bun run typecheck"
  run_command_check "all-web-ui test" sh -c "cd \"$ALL_WEB_UI_DIR\" && bun test"
  run_command_check "all-web-ui build" sh -c "cd \"$ALL_WEB_UI_DIR\" && bun run build"
  run_command_check "rich/web typecheck" sh -c "cd \"$RICH_WEB_DIR\" && bun run typecheck"
  run_command_check "rich/web test" sh -c "cd \"$RICH_WEB_DIR\" && bun run test -- --no-file-parallelism --maxWorkers=1"
  run_command_check "rich/web build" sh -c "cd \"$RICH_WEB_DIR\" && NEXT_PUBLIC_SUPABASE_URL=https://example.supabase.co NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=sb_publishable_test SUPABASE_SERVICE_ROLE_KEY=service-role-test GOOGLE_OAUTH_CLIENT_ID=client-id GOOGLE_OAUTH_CLIENT_SECRET=client-secret GOOGLE_TOKEN_ENCRYPTION_KEY=0123456789abcdef0123456789abcdef GOOGLE_SHEETS_SPREADSHEET_ID=sheet-id bun run build"
  run_command_check "keelim-vercel typecheck" sh -c "cd \"$KEELIM_VERCEL_DIR\" && bun run typecheck"
  run_command_check "keelim-vercel lint" sh -c "cd \"$KEELIM_VERCEL_DIR\" && bun run lint"
  run_command_check "keelim-vercel verify:maintenance" sh -c "cd \"$KEELIM_VERCEL_DIR\" && bun run verify:maintenance"
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
