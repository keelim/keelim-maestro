#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-status}"

if [[ "$MODE" != "status" && "$MODE" != "update" ]]; then
  cat <<'EOF'
Usage:
  scripts/update-subrepos.sh [status|update]

Modes:
  status  Show branch / dirty / ahead-behind summary for tracked child repos
  update  Fast-forward pull only for clean repos on main/master/develop branches
EOF
  exit 1
fi

ROOT_DIR="$(git rev-parse --show-toplevel)"
cd "$ROOT_DIR"

declare -a REPOS=()

append_unique_repo() {
  local repo_path="$1"
  local existing

  for existing in "${REPOS[@]-}"; do
    if [[ "$existing" == "$repo_path" ]]; then
      return 0
    fi
  done

  REPOS+=("$repo_path")
}

while read -r _ path; do
  if [[ -n "${path:-}" ]]; then
    append_unique_repo "$path"
  fi
done < <(git config -f .gitmodules --get-regexp '^submodule\..*\.path$' 2>/dev/null || true)

for extra in rich quant; do
  if [[ -d "$extra/.git" ]]; then
    append_unique_repo "$extra"
  fi
done

resolve_branch() {
  local repo_path="$1"
  local branch=""
  local repo_name
  repo_name="$(basename "$repo_path")"

  branch="$(git config -f .gitmodules --get "submodule.${repo_name}.branch" 2>/dev/null || true)"
  if [[ -n "$branch" && "$branch" != "." ]]; then
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

  printf '%s\n' ""
}

print_repo_status() {
  local repo_path="$1"
  local current_branch dirty remote_url upstream ahead behind target_branch

  current_branch="$(git -C "$repo_path" symbolic-ref --quiet --short HEAD 2>/dev/null || echo "DETACHED")"
  target_branch="$(resolve_branch "$repo_path")"
  dirty="clean"
  if [[ -n "$(git -C "$repo_path" status --porcelain 2>/dev/null)" ]]; then
    dirty="dirty"
  fi

  remote_url="$(git -C "$repo_path" remote get-url origin 2>/dev/null || true)"
  upstream="$(git -C "$repo_path" rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
  ahead="-"
  behind="-"

  if [[ -n "$upstream" ]]; then
    read -r ahead behind < <(git -C "$repo_path" rev-list --left-right --count "HEAD...$upstream")
  fi

  printf '%-24s branch=%-10s target=%-10s state=%-5s ahead=%-4s behind=%-4s remote=%s\n' \
    "$repo_path" "$current_branch" "${target_branch:-n/a}" "$dirty" "$ahead" "$behind" "${remote_url:-none}"
}

update_repo() {
  local repo_path="$1"
  local current_branch target_branch remote_url upstream ahead behind

  current_branch="$(git -C "$repo_path" symbolic-ref --quiet --short HEAD 2>/dev/null || echo "DETACHED")"
  target_branch="$(resolve_branch "$repo_path")"
  remote_url="$(git -C "$repo_path" remote get-url origin 2>/dev/null || true)"
  upstream="$(git -C "$repo_path" rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
  ahead="0"
  behind="0"

  if [[ -n "$upstream" ]]; then
    read -r ahead behind < <(git -C "$repo_path" rev-list --left-right --count "HEAD...$upstream")
  fi

  if [[ -z "$remote_url" ]]; then
    printf '[skip] %-24s no origin remote\n' "$repo_path"
    return 0
  fi

  if [[ -n "$(git -C "$repo_path" status --porcelain 2>/dev/null)" ]]; then
    printf '[skip] %-24s dirty working tree\n' "$repo_path"
    return 0
  fi

  if [[ -z "$target_branch" ]]; then
    printf '[skip] %-24s no supported target branch (main/master/develop)\n' "$repo_path"
    return 0
  fi

  if [[ "$current_branch" != "$target_branch" ]]; then
    printf '[skip] %-24s current branch=%s target=%s\n' "$repo_path" "$current_branch" "$target_branch"
    return 0
  fi

  if [[ "$ahead" != "0" ]]; then
    printf '[skip] %-24s local commits ahead of upstream (%s)\n' "$repo_path" "$ahead"
    return 0
  fi

  printf '[fetch] %-23s origin\n' "$repo_path"
  git -C "$repo_path" fetch --prune origin

  printf '[pull]  %-23s %s\n' "$repo_path" "$target_branch"
  git -C "$repo_path" pull --ff-only origin "$target_branch"
}

printf 'Root: %s\n' "$ROOT_DIR"
printf 'Mode: %s\n\n' "$MODE"

for repo in "${REPOS[@]}"; do
  if [[ ! -d "$repo/.git" && ! -f "$repo/.git" ]]; then
    printf '[skip] %-24s not a git worktree\n' "$repo"
    continue
  fi

  if [[ "$MODE" == "status" ]]; then
    print_repo_status "$repo"
  else
    update_repo "$repo"
  fi
done

if [[ "$MODE" == "update" ]]; then
  cat <<'EOF'

Done.
Review next:
  git status --short
  git status --ignore-submodules=none --short
  git submodule status
EOF
fi
