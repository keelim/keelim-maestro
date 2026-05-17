#!/bin/sh
set -eu

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

ALL_WEB_UI_PACKAGE="@keelim/all-web-ui"
GITHUB_PACKAGES_REGISTRY="@keelim:registry=https://npm.pkg.github.com"

ALL_WEB_UI_DIR="$ROOT/all-web-ui"
KEELIM_VERCEL_DIR="$ROOT/keelim-vercel"
RICH_WEB_DIR="$ROOT/rich/web"
ALL_WEB_UI_VERSION="$(
  jq -r '.version // empty' "$ALL_WEB_UI_DIR/package.json" 2>/dev/null || true
)"

VERIFY_LOG="${TMPDIR:-/tmp}/keelim-maestro-shared-ui-contract-$$.log"
VERIFIER_STATUS="MISSING"
VERIFIER_PASS_COUNT="0"
VERIFIER_FAIL_COUNT="0"
VERIFIER_NOTE="scripts/verify-all-web-ui-integration.sh is absent"

trap 'rm -f "$VERIFY_LOG"' EXIT INT HUP TERM

print_row() {
  printf '| %s | %s | %s |\n' "$1" "$2" "$3"
}

has_tool() {
  command -v "$1" >/dev/null 2>&1
}

json_value() {
  package_json="$1"
  expression="$2"

  if [ -f "$package_json" ] && has_tool jq; then
    jq -r "$expression" "$package_json" 2>/dev/null || true
  fi
}

dependency_spec() {
  package_json="$1"

  if [ -f "$package_json" ] && has_tool jq; then
    jq -r --arg package_name "$ALL_WEB_UI_PACKAGE" '
      (.dependencies // {})[$package_name]
      // (.devDependencies // {})[$package_name]
      // (.peerDependencies // {})[$package_name]
      // empty
    ' "$package_json" 2>/dev/null || true
  fi
}

package_script_exists() {
  package_json="$1"
  script_name="$2"

  [ -f "$package_json" ] &&
    has_tool jq &&
    jq -e --arg script_name "$script_name" '(.scripts // {})[$script_name]' "$package_json" >/dev/null 2>&1
}

script_bundle_status() {
  package_json="$1"
  shift

  missing=""
  for script_name in "$@"; do
    if ! package_script_exists "$package_json" "$script_name"; then
      missing="${missing}${missing:+, }${script_name}"
    fi
  done

  if [ -z "$missing" ]; then
    printf 'READY'
  else
    printf 'MISSING %s' "$missing"
  fi
}

count_fixed_code_hits() {
  target_dir="$1"
  pattern="$2"

  if [ -d "$target_dir" ] && has_tool rg; then
    rg -n --fixed-strings "$pattern" "$target_dir" \
      -g '*.css' \
      -g '*.js' \
      -g '*.mjs' \
      -g '*.ts' \
      -g '*.tsx' 2>/dev/null |
      wc -l |
      tr -d '[:space:]'
  else
    printf '0'
  fi
}

file_has_fixed_string() {
  file_path="$1"
  needle="$2"

  [ -f "$file_path" ] && has_tool rg && rg -q --fixed-strings "$needle" "$file_path"
}

dir_has_fixed_string() {
  target_dir="$1"
  needle="$2"

  [ -d "$target_dir" ] && has_tool rg && rg -q --fixed-strings "$needle" "$target_dir"
}

registry_mapping_status() {
  package_dir="$1"

  if [ ! -d "$package_dir" ]; then
    printf 'MISSING repo'
  elif [ ! -f "$package_dir/.npmrc" ]; then
    printf 'FAIL no .npmrc'
  elif file_has_fixed_string "$package_dir/.npmrc" "$GITHUB_PACKAGES_REGISTRY"; then
    printf 'PASS GitHub Packages'
  else
    printf 'FAIL registry mapping drift'
  fi
}

dependency_status() {
  package_json="$1"
  spec="$(dependency_spec "$package_json")"

  if [ -z "$spec" ]; then
    printf 'FAIL missing'
  elif [ "$spec" = "$ALL_WEB_UI_VERSION" ]; then
    printf 'PASS %s' "$spec"
  else
    printf 'FAIL %s' "$spec"
  fi
}

style_import_status() {
  target_dir="$1"
  required_one="$2"
  required_two="${3:-}"

  missing=""
  for required in "$required_one" "$required_two"; do
    [ -z "$required" ] && continue
    if ! dir_has_fixed_string "$target_dir" "$ALL_WEB_UI_PACKAGE/$required"; then
      missing="${missing}${missing:+, }${required}"
    fi
  done

  if [ -z "$missing" ]; then
    printf 'PASS %s%s' "$required_one" "${required_two:+ + $required_two}"
  else
    printf 'MANUAL missing %s' "$missing"
  fi
}

visual_readiness_status() {
  package_dir="$1"

  if [ ! -d "$package_dir" ]; then
    printf 'MISSING repo'
    return
  fi

  package_json="$package_dir/package.json"
  if [ -f "$package_json" ] && has_tool jq &&
    jq -e '
      [(.scripts // {}) | to_entries[]? |
        select((.key + " " + .value) | test("visual|e2e|playwright|screenshot"; "i"))]
      | length > 0
    ' "$package_json" >/dev/null 2>&1; then
    printf 'READY automated script'
    return
  fi

  if ls "$package_dir"/playwright.config.* >/dev/null 2>&1; then
    printf 'READY playwright config'
    return
  fi

  printf 'MANUAL no automated visual gate'
}

run_static_verifier() {
  if [ ! -f "$ROOT/scripts/verify-all-web-ui-integration.sh" ]; then
    return
  fi

  if sh "$ROOT/scripts/verify-all-web-ui-integration.sh" >"$VERIFY_LOG" 2>&1; then
    VERIFIER_STATUS="PASS"
  else
    VERIFIER_STATUS="FAIL"
  fi

  VERIFIER_PASS_COUNT="$(grep -c '^PASS  ' "$VERIFY_LOG" 2>/dev/null || true)"
  VERIFIER_FAIL_COUNT="$(grep -c '^FAIL  ' "$VERIFY_LOG" 2>/dev/null || true)"
  VERIFIER_NOTE="static verifier PASS=${VERIFIER_PASS_COUNT} FAIL=${VERIFIER_FAIL_COUNT}"
}

print_header() {
  cat <<EOF
# Shared UI Contract Control Tower

- Workspace root: \`$ROOT\`
- Provider package: \`$ALL_WEB_UI_PACKAGE@$ALL_WEB_UI_VERSION\`
- Report mode: read-only observation; child repositories are not mutated
- Strict static gate: \`sh scripts/verify-all-web-ui-integration.sh\`

EOF
}

print_provider_table() {
  package_json="$ALL_WEB_UI_DIR/package.json"
  package_name="$(json_value "$package_json" '.name // ""')"
  package_version="$(json_value "$package_json" '.version // ""')"
  package_private="$(json_value "$package_json" '.private | tostring')"
  package_registry="$(json_value "$package_json" '.publishConfig.registry // ""')"
  export_count="$(json_value "$package_json" '(.exports // {}) | length')"
  side_effect_count="$(json_value "$package_json" '(.sideEffects // []) | length')"
  manifest_count="0"

  if [ -f "$ALL_WEB_UI_DIR/src/manifest.ts" ] && has_tool rg; then
    manifest_count="$(
      rg -n --fixed-strings "exportPath:" "$ALL_WEB_UI_DIR/src/manifest.ts" 2>/dev/null |
        wc -l |
        tr -d '[:space:]'
    )"
  fi

  printf '## Provider\n\n'
  printf '| signal | status | evidence |\n'
  printf '| --- | --- | --- |\n'

  if [ "$package_name" = "$ALL_WEB_UI_PACKAGE" ] &&
    [ "$package_version" = "$ALL_WEB_UI_VERSION" ] &&
    [ "$package_private" = "false" ] &&
    [ "$package_registry" = "https://npm.pkg.github.com" ]; then
    print_row "package identity" "PASS" "\`$package_name@$package_version\`, publishConfig GitHub Packages"
  else
    print_row "package identity" "FAIL" "name=\`${package_name:-missing}\`, version=\`${package_version:-missing}\`, private=\`${package_private:-missing}\`, registry=\`${package_registry:-missing}\`"
  fi

  if [ -n "$export_count" ] && [ "$export_count" -gt 0 ]; then
    print_row "package exports" "PASS" "\`package.json\` exposes $export_count export entries"
  else
    print_row "package exports" "FAIL" "No package exports detected"
  fi

  if [ "$manifest_count" -gt 0 ]; then
    print_row "component manifest" "PASS" "\`src/manifest.ts\` lists $manifest_count exportPath entries"
  else
    print_row "component manifest" "FAIL" "\`src/manifest.ts\` missing or empty"
  fi

  missing_styles=""
  for style_file in \
    src/styles/styles.css \
    src/styles/spacing.css \
    src/styles/themes/finance.css \
    src/styles/themes/admin-bw.css
  do
    if [ ! -f "$ALL_WEB_UI_DIR/$style_file" ]; then
      missing_styles="${missing_styles}${missing_styles:+, }${style_file}"
    fi
  done

  if [ -z "$missing_styles" ]; then
    print_row "style and theme entrypoints" "PASS" "styles, spacing, finance theme, admin-bw theme exist"
  else
    print_row "style and theme entrypoints" "FAIL" "Missing $missing_styles"
  fi

  if [ -n "$side_effect_count" ] && [ "$side_effect_count" -gt 0 ]; then
    print_row "CSS sideEffects" "PASS" "\`package.json\` lists $side_effect_count side-effect entries"
  else
    print_row "CSS sideEffects" "MANUAL" "No sideEffects list detected"
  fi

  printf '\n'
}

print_consumer_row() {
  consumer_name="$1"
  package_dir="$2"
  required_style="$3"
  required_theme="${4:-}"

  package_json="$package_dir/package.json"
  imports_count="$(count_fixed_code_hits "$package_dir" "$ALL_WEB_UI_PACKAGE")"
  dependency_cell="$(dependency_status "$package_json")"
  registry_cell="$(registry_mapping_status "$package_dir")"
  style_cell="$(style_import_status "$package_dir" "$required_style" "$required_theme")"

  if [ "$imports_count" -gt 0 ]; then
    import_cell="PASS ${imports_count} code hits"
  else
    import_cell="WARN no scoped package code hits"
  fi

  print_row "$consumer_name" "$dependency_cell" "$registry_cell; $import_cell; $style_cell"
}

print_consumers_table() {
  printf '## Consumers\n\n'
  printf '| consumer | dependency | contract evidence |\n'
  printf '| --- | --- | --- |\n'
  print_consumer_row "keelim-vercel" "$KEELIM_VERCEL_DIR" "styles.css" "themes/finance.css"
  print_consumer_row "rich/web" "$RICH_WEB_DIR" "styles.css" "themes/admin-bw.css"
  printf '\n'
}

print_static_verifier_table() {
  printf '## Static Verifier\n\n'
  printf '| command | status | evidence |\n'
  printf '| --- | --- | --- |\n'
  print_row "\`sh scripts/verify-all-web-ui-integration.sh\`" "$VERIFIER_STATUS" "$VERIFIER_NOTE"
  printf '\n'
}

print_canary_table() {
  printf '## Build Canary Inventory\n\n'
  printf '| surface | readiness | command |\n'
  printf '| --- | --- | --- |\n'
  print_row "root static contract" "$VERIFIER_STATUS" "\`sh scripts/verify-all-web-ui-integration.sh\`"
  print_row "root full contract" "MANUAL" "\`sh scripts/verify-all-web-ui-integration.sh --full\`"
  print_row "all-web-ui package" "$(script_bundle_status "$ALL_WEB_UI_DIR/package.json" typecheck test build)" "\`cd all-web-ui && bun run typecheck && bun test && bun run build\`"
  print_row "rich/web consumer" "$(script_bundle_status "$RICH_WEB_DIR/package.json" typecheck test build)" "\`cd rich/web && bun run typecheck && bun run test\`; env-bound build is covered by \`sh scripts/verify-all-web-ui-integration.sh --full\`"
  print_row "keelim-vercel consumer" "$(script_bundle_status "$KEELIM_VERCEL_DIR/package.json" typecheck lint verify:maintenance build)" "\`cd keelim-vercel && bun run typecheck && bun run lint && bun run verify:maintenance && bun run build\`"
  printf '\n'
}

print_visual_table() {
  printf '## Visual Regression Readiness\n\n'
  printf '| surface | status | evidence |\n'
  printf '| --- | --- | --- |\n'
  print_row "all-web-ui" "$(visual_readiness_status "$ALL_WEB_UI_DIR")" "Provider has design/token assets; automated visual regression is a follow-up unless READY"
  print_row "keelim-vercel" "$(visual_readiness_status "$KEELIM_VERCEL_DIR")" "Finance theme consumer"
  print_row "rich/web" "$(visual_readiness_status "$RICH_WEB_DIR")" "Admin-bw theme consumer"
  printf '\n'
}

print_footer() {
  cat <<'EOF'
## Reading The Report

- `PASS` means the root can observe the expected contract signal now.
- `FAIL` means the existing strict verifier or package metadata found drift.
- `MANUAL` means the signal is intentionally inventoried here but is not an automated gate yet.
- This report exits `0` when it can emit observations; use `scripts/verify-all-web-ui-integration.sh` for strict static failure semantics.
EOF
}

main() {
  run_static_verifier
  print_header
  print_provider_table
  print_consumers_table
  print_static_verifier_table
  print_canary_table
  print_visual_table
  print_footer
}

main "$@"
