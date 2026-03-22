#!/bin/sh
set -eu

print_usage() {
  cat <<'EOF'
Usage:
  scripts/update-subrepos.sh [status]
  scripts/update-subrepos.sh update [--dry-run]
  scripts/update-subrepos.sh dry-run

Modes:
  status   Show branch / dirty / ahead-behind summary for tracked child repos
  update   Fast-forward pull only for clean repos on main/master/develop branches
  dry-run  Preview which repos would be fetched / pulled without changing anything
EOF
}

MODE="status"
DRY_RUN="0"

case "${1:-status}" in
  status)
    MODE="status"
    ;;
  update)
    MODE="update"
    ;;
  dry-run|--dry-run)
    MODE="update"
    DRY_RUN="1"
    ;;
  *)
    print_usage
    exit 1
    ;;
esac

if [ "${2:-}" = "--dry-run" ]; then
  DRY_RUN="1"
fi

if [ "${2:-}" ] && [ "${2:-}" != "--dry-run" ]; then
  print_usage
  exit 1
fi

ROOT_DIR="$(git rev-parse --show-toplevel)"
cd "$ROOT_DIR"

list_repo_paths() {
  {
    git config -f .gitmodules --get-regexp '^submodule\..*\.path$' 2>/dev/null | awk '{print $2}' || true
    for extra in all-web-ui rich quant; do
      if [ -d "$extra/.git" ]; then
        printf '%s\n' "$extra"
      fi
    done
  } | awk 'NF && !seen[$0]++'
}

resolve_branch() {
  repo_path="$1"
  repo_name="$(basename "$repo_path")"
  branch="$(git config -f .gitmodules --get "submodule.${repo_name}.branch" 2>/dev/null || true)"

  if [ -n "$branch" ] && [ "$branch" != "." ]; then
    printf '%s\n' "$branch"
    return 0
  fi

  branch="$(git -C "$repo_path" symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
  case "$branch" in
    main|master|develop)
      printf '%s\n' "$branch"
      return 0
      ;;
  esac

  branch="$(git -C "$repo_path" symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null || true)"
  branch="${branch#origin/}"
  case "$branch" in
    main|master|develop)
      printf '%s\n' "$branch"
      return 0
      ;;
  esac

  printf '\n'
}

repo_exists() {
  repo_path="$1"
  [ -d "$repo_path/.git" ] || [ -f "$repo_path/.git" ]
}

status_ahead_behind() {
  repo_path="$1"
  upstream="$(git -C "$repo_path" rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"

  if [ -n "$upstream" ]; then
    set -- $(git -C "$repo_path" rev-list --left-right --count "HEAD...$upstream")
    printf '%s %s\n' "${1:-0}" "${2:-0}"
  else
    printf '%s %s\n' "-" "-"
  fi
}

update_ahead_behind() {
  repo_path="$1"
  upstream="$(git -C "$repo_path" rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"

  if [ -n "$upstream" ]; then
    set -- $(git -C "$repo_path" rev-list --left-right --count "HEAD...$upstream")
    printf '%s %s\n' "${1:-0}" "${2:-0}"
  else
    printf '0 0\n'
  fi
}

print_repo_status() {
  repo_path="$1"
  current_branch="$(git -C "$repo_path" symbolic-ref --quiet --short HEAD 2>/dev/null || echo "DETACHED")"
  target_branch="$(resolve_branch "$repo_path")"
  dirty="clean"

  if [ -n "$(git -C "$repo_path" status --porcelain 2>/dev/null)" ]; then
    dirty="dirty"
  fi

  remote_url="$(git -C "$repo_path" remote get-url origin 2>/dev/null || true)"
  set -- $(status_ahead_behind "$repo_path")
  ahead="$1"
  behind="$2"

  if [ -z "$target_branch" ]; then
    target_branch="n/a"
  fi

  if [ -z "$remote_url" ]; then
    remote_url="none"
  fi

  printf '%-24s branch=%-10s target=%-10s state=%-5s ahead=%-4s behind=%-4s remote=%s\n' \
    "$repo_path" "$current_branch" "$target_branch" "$dirty" "$ahead" "$behind" "$remote_url"
}

update_repo() {
  repo_path="$1"
  current_branch="$(git -C "$repo_path" symbolic-ref --quiet --short HEAD 2>/dev/null || echo "DETACHED")"
  target_branch="$(resolve_branch "$repo_path")"
  remote_url="$(git -C "$repo_path" remote get-url origin 2>/dev/null || true)"

  if [ -z "$remote_url" ]; then
    printf '[skip] %-24s no origin remote\n' "$repo_path"
    return 0
  fi

  if [ -n "$(git -C "$repo_path" status --porcelain 2>/dev/null)" ]; then
    printf '[skip] %-24s dirty working tree\n' "$repo_path"
    return 0
  fi

  if [ -z "$target_branch" ]; then
    printf '[skip] %-24s no supported target branch (main/master/develop)\n' "$repo_path"
    return 0
  fi

  if [ "$current_branch" != "$target_branch" ]; then
    printf '[skip] %-24s current branch=%s target=%s\n' "$repo_path" "$current_branch" "$target_branch"
    return 0
  fi

  set -- $(update_ahead_behind "$repo_path")
  ahead="$1"

  if [ "$ahead" != "0" ]; then
    printf '[skip] %-24s local commits ahead of upstream (%s)\n' "$repo_path" "$ahead"
    return 0
  fi

  if [ "$DRY_RUN" = "1" ]; then
    printf '[dry-run] %-21s would fetch origin\n' "$repo_path"
    printf '[dry-run] %-21s would pull --ff-only origin %s\n' "$repo_path" "$target_branch"
    return 0
  fi

  printf '[fetch] %-23s origin\n' "$repo_path"
  git -C "$repo_path" fetch --prune origin

  printf '[pull]  %-23s %s\n' "$repo_path" "$target_branch"
  git -C "$repo_path" pull --ff-only origin "$target_branch"
}

printf 'Root: %s\n' "$ROOT_DIR"
if [ "$MODE" = "update" ] && [ "$DRY_RUN" = "1" ]; then
  printf 'Mode: dry-run\n\n'
else
  printf 'Mode: %s\n\n' "$MODE"
fi

list_repo_paths | while IFS= read -r repo; do
  [ -n "$repo" ] || continue

  if ! repo_exists "$repo"; then
    printf '[skip] %-24s not a git worktree\n' "$repo"
    continue
  fi

  if [ "$MODE" = "status" ]; then
    print_repo_status "$repo"
  else
    update_repo "$repo"
  fi
done

if [ "$MODE" = "update" ] && [ "$DRY_RUN" = "0" ]; then
  cat <<'EOF'

Done.
Review next:
  git status --short
  git status --ignore-submodules=none --short
  git submodule status
EOF
fi
