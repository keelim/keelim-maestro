#!/bin/sh
set -eu

DEFAULT_CODEGRAPH_BIN="/Users/keelim/.bun/install/global/node_modules/@colbymchenry/codegraph-darwin-arm64/bin/codegraph"

print_usage() {
  cat <<'EOF'
Usage:
  scripts/codegraph.sh list
  scripts/codegraph.sh status [all|repo]
  scripts/codegraph.sh files <repo> [codegraph files options]
  scripts/codegraph.sh context <repo> <task>
  scripts/codegraph.sh query <repo> <search>
  scripts/codegraph.sh affected <repo> [files...]
  scripts/codegraph.sh sync [all|repo]
  scripts/codegraph.sh root-check

Repos:
  all
  all-web-ui
  android-support
  Keelim-Knowledge-Vault
  keelim-plugin
  keelim-vercel
  rich

Notes:
  root, quant, toto, tools, and tools/crawler are intentionally excluded targets.
  This helper never initializes .codegraph/; run codegraph init -i explicitly
  inside the intended child repo when a graph is missing.
EOF
}

find_codegraph() {
  if [ -n "${CODEGRAPH_BIN:-}" ]; then
    if [ -x "$CODEGRAPH_BIN" ]; then
      printf '%s\n' "$CODEGRAPH_BIN"
      return 0
    fi

    printf 'CODEGRAPH_BIN is set but not executable: %s\n' "$CODEGRAPH_BIN" >&2
    return 127
  fi

  if command -v codegraph >/dev/null 2>&1; then
    command -v codegraph
    return 0
  fi

  if [ -x "$DEFAULT_CODEGRAPH_BIN" ]; then
    printf '%s\n' "$DEFAULT_CODEGRAPH_BIN"
    return 0
  fi

  printf 'CodeGraph CLI not found. Set CODEGRAPH_BIN or install/expose codegraph on PATH.\n' >&2
  return 127
}

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

CODEGRAPH="$(find_codegraph)"
CHILD_REPOS="all all-web-ui android-support Keelim-Knowledge-Vault keelim-plugin keelim-vercel rich"

is_child_repo() {
  case "$1" in
    all|all-web-ui|android-support|Keelim-Knowledge-Vault|keelim-plugin|keelim-vercel|rich)
      return 0
      ;;
  esac

  return 1
}

repo_path() {
  repo="$1"

  if ! is_child_repo "$repo"; then
    case "$repo" in
      ""|.|root|keelim-maestro|"$ROOT")
        printf 'root is not a child CodeGraph target; use root-check for root guidance.\n' >&2
        ;;
      quant|toto|tools|tools/crawler)
        printf '%s is intentionally excluded from child CodeGraph dispatch.\n' "$repo" >&2
        ;;
      *)
        printf 'Unknown CodeGraph child repo: %s\n' "$repo" >&2
        ;;
    esac
    return 2
  fi

  printf '%s/%s\n' "$ROOT" "$repo"
}

repo_present() {
  path="$1"
  [ -d "$path/.git" ] || [ -f "$path/.git" ]
}

graph_present() {
  path="$1"
  [ -d "$path/.codegraph" ]
}

require_repo() {
  repo="$1"
  path="$(repo_path "$repo")"

  if ! repo_present "$path"; then
    printf '%s is absent: %s\n' "$repo" "$path" >&2
    return 1
  fi

  printf '%s\n' "$path"
}

require_graph() {
  repo="$1"
  path="$(require_repo "$repo")"

  if ! graph_present "$path"; then
    printf '%s is missing .codegraph/. Run: %s init -i %s\n' "$repo" "$CODEGRAPH" "$path" >&2
    return 1
  fi

  printf '%s\n' "$path"
}

print_list() {
  printf 'Root: %s\n' "$ROOT"
  printf 'CodeGraph: %s\n\n' "$CODEGRAPH"
  printf '%-24s %-8s %-12s %s\n' "repo" "present" ".codegraph" "path"

  for repo in $CHILD_REPOS; do
    path="$ROOT/$repo"
    present="absent"
    graph="missing"

    if repo_present "$path"; then
      present="present"
    fi

    if graph_present "$path"; then
      graph="present"
    fi

    printf '%-24s %-8s %-12s %s\n' "$repo" "$present" "$graph" "$path"
  done

  printf '%-24s %-8s %-12s %s\n' "quant" "excluded" "n/a" "$ROOT/quant"
  printf '%-24s %-8s %-12s %s\n' "tools" "excluded" "n/a" "$ROOT/tools"
  printf '%-24s %-8s %-12s %s\n' "tools/crawler" "excluded" "n/a" "$ROOT/tools/crawler"
}

status_repo() {
  repo="$1"
  path="$(repo_path "$repo")"

  printf '=== %s ===\n' "$repo"
  if ! repo_present "$path"; then
    printf '{"repo":"%s","projectPath":"%s","present":false,"initialized":false}\n' "$repo" "$path"
    return 0
  fi

  "$CODEGRAPH" status --json "$path"
}

status_target() {
  target="${1:-all}"

  if [ "$target" = "all" ]; then
    for repo in $CHILD_REPOS; do
      status_repo "$repo"
    done
    return 0
  fi

  status_repo "$target"
}

sync_repo() {
  repo="$1"
  path="$(require_graph "$repo")"
  printf '=== %s ===\n' "$repo"
  "$CODEGRAPH" sync "$path"
}

sync_target() {
  target="${1:-all}"
  failures=0

  if [ "$target" = "all" ]; then
    for repo in $CHILD_REPOS; do
      if ! sync_repo "$repo"; then
        failures=$((failures + 1))
      fi
    done

    [ "$failures" -eq 0 ]
    return $?
  fi

  sync_repo "$target"
}

root_check() {
  printf 'Root: %s\n' "$ROOT"

  if [ ! -d "$ROOT/.codegraph" ]; then
    cat <<'EOF'
Root .codegraph/ is absent.
Recommended operation: keep root CodeGraph deferred and use this dispatcher to call child repo graphs with --path.
EOF
    return 0
  fi

  printf 'Root .codegraph/ exists. Checking whether child source appears in the root graph...\n\n'
  tmp_file="${TMPDIR:-/tmp}/codegraph-root-files-$$.txt"
  "$CODEGRAPH" files --path "$ROOT" --max-depth 2 >"$tmp_file"
  cat "$tmp_file"

  found_children=""
  for repo in $CHILD_REPOS; do
    if grep -E "(├──|└──) ${repo}($|[[:space:]])" "$tmp_file" >/dev/null 2>&1; then
      found_children="${found_children} ${repo}"
    fi
  done
  rm -f "$tmp_file"

  if [ -n "$found_children" ]; then
    printf '\nWarning: root graph includes child source trees:%s\n' "$found_children" >&2
    printf 'Recommended action: codegraph uninit --force %s\n' "$ROOT" >&2
    return 1
  fi

  printf '\nRoot graph does not show child repos at max depth 2.\n'
}

COMMAND="${1:-}"
if [ -z "$COMMAND" ]; then
  print_usage
  exit 2
fi
shift || true

case "$COMMAND" in
  list)
    [ "$#" -eq 0 ] || { print_usage; exit 2; }
    print_list
    ;;
  status)
    status_target "${1:-all}"
    ;;
  files)
    [ "$#" -ge 1 ] || { print_usage; exit 2; }
    repo="$1"
    shift
    path="$(require_graph "$repo")"
    "$CODEGRAPH" files --path "$path" "$@"
    ;;
  context)
    [ "$#" -ge 2 ] || { print_usage; exit 2; }
    repo="$1"
    shift
    path="$(require_graph "$repo")"
    "$CODEGRAPH" context --path "$path" "$*"
    ;;
  query)
    [ "$#" -ge 2 ] || { print_usage; exit 2; }
    repo="$1"
    shift
    path="$(require_graph "$repo")"
    "$CODEGRAPH" query --path "$path" "$*"
    ;;
  affected)
    [ "$#" -ge 1 ] || { print_usage; exit 2; }
    repo="$1"
    shift
    path="$(require_graph "$repo")"
    "$CODEGRAPH" affected --path "$path" "$@"
    ;;
  sync)
    sync_target "${1:-all}"
    ;;
  root-check)
    [ "$#" -eq 0 ] || { print_usage; exit 2; }
    root_check
    ;;
  -h|--help|help)
    print_usage
    ;;
  *)
    print_usage
    exit 2
    ;;
esac
