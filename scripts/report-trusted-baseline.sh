#!/bin/sh
set -eu

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

sanitize_cell() {
  printf '%s' "$1" | tr '|' '/'
}

list_package_workspaces() {
  awk '
    /"workspaces"[[:space:]]*:/ { in_workspaces = 1; next }
    in_workspaces && /\]/ { in_workspaces = 0 }
    in_workspaces {
      gsub(/[",]/, "")
      for (i = 1; i <= NF; i++) {
        if ($i != "") print $i
      }
    }
  ' package.json
}

list_uv_members() {
  awk '
    /^\[tool\.uv\.workspace\]/ { in_workspace = 1; next }
    /^\[/ && in_workspace { in_workspace = 0 }
    in_workspace && /members[[:space:]]*=/ { in_members = 1; next }
    in_workspace && in_members && /\]/ { in_members = 0 }
    in_workspace && in_members {
      gsub(/[",]/, "")
      for (i = 1; i <= NF; i++) {
        if ($i != "") print $i
      }
    }
  ' pyproject.toml
}

list_registered_paths() {
  git config -f .gitmodules --get-regexp '^submodule\..*\.path$' 2>/dev/null | awk '{print $2}' || true
}

list_report_paths() {
  {
    list_registered_paths
    for extra in all-web-ui rich quant; do
      if [ -e "$extra" ]; then
        printf '%s\n' "$extra"
      fi
    done
  } | awk 'NF && !seen[$0]++'
}

is_registered_path() {
  path="$1"
  list_registered_paths | grep -Fx "$path" >/dev/null 2>&1
}

repo_exists() {
  path="$1"
  [ -d "$path/.git" ] || [ -f "$path/.git" ]
}

submodule_branch_for_path() {
  path="$1"
  git config -f .gitmodules --get-regexp '^submodule\..*\.path$' 2>/dev/null | while read -r key value; do
    [ "$value" = "$path" ] || continue
    section="${key#submodule.}"
    section="${section%.path}"
    git config -f .gitmodules --get "submodule.${section}.branch" 2>/dev/null || true
    break
  done
}

resolve_target_branch() {
  path="$1"
  branch="$(submodule_branch_for_path "$path")"
  if [ -n "$branch" ] && [ "$branch" != "." ]; then
    printf '%s\n' "$branch"
    return 0
  fi

  if repo_exists "$path"; then
    branch="$(git -C "$path" symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
    case "$branch" in
      main|master|develop)
        printf '%s\n' "$branch"
        return 0
        ;;
    esac

    branch="$(git -C "$path" symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null || true)"
    branch="${branch#origin/}"
    case "$branch" in
      main|master|develop)
        printf '%s\n' "$branch"
        return 0
        ;;
    esac
  fi

  printf 'n/a\n'
}

workspace_membership_for_path() {
  path="$1"
  members="$2"

  printf '%s\n' "$members" | while IFS= read -r member; do
    [ -n "$member" ] || continue
    case "$member" in
      "$path")
        printf '%s\n' "$member"
        ;;
      "$path"/*)
        printf '%s\n' "$member"
        ;;
    esac
  done | awk 'BEGIN { result = "no" } NF { if (result == "no") result = $0; else result = result "," $0 } END { print result }'
}

gitlink_for_path() {
  path="$1"
  line="$(git ls-files --stage -- "$path" 2>/dev/null | awk '$1 == "160000" { print $2; exit }')"
  if [ -n "$line" ]; then
    printf 'yes:%s\n' "$(printf '%s' "$line" | cut -c1-8)"
  else
    printf 'no\n'
  fi
}

ahead_behind_for_path() {
  path="$1"
  upstream="$(git -C "$path" rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
  if [ -n "$upstream" ]; then
    set -- $(git -C "$path" rev-list --left-right --count "HEAD...$upstream")
    printf '%s %s\n' "${1:-0}" "${2:-0}"
  else
    printf -- '- -\n'
  fi
}

registration_for_path() {
  path="$1"
  if is_registered_path "$path"; then
    printf 'registered-submodule\n'
  else
    case "$path" in
      quant)
        printf 'excluded-local\n'
        ;;
      *)
        printf 'autonomous\n'
        ;;
    esac
  fi
}

append_blocker() {
  current="$1"
  next="$2"
  if [ "$current" = "none" ]; then
    printf '%s\n' "$next"
  else
    printf '%s,%s\n' "$current" "$next"
  fi
}

print_row() {
  path="$1"
  registration="$(registration_for_path "$path")"
  gitlink="$(gitlink_for_path "$path")"
  bun_membership="$(workspace_membership_for_path "$path" "$BUN_WORKSPACES")"
  uv_membership="$(workspace_membership_for_path "$path" "$UV_MEMBERS")"

  current_branch="missing"
  target_branch="n/a"
  state="missing"
  ahead="-"
  behind="-"
  remote="none"
  eligibility="blocked"
  blocker="missing-worktree"

  if repo_exists "$path"; then
    current_branch="$(git -C "$path" symbolic-ref --quiet --short HEAD 2>/dev/null || printf 'DETACHED')"
    target_branch="$(resolve_target_branch "$path")"
    state="clean"
    if [ -n "$(git -C "$path" status --porcelain 2>/dev/null)" ]; then
      state="dirty"
    fi
    remote="$(git -C "$path" remote get-url origin 2>/dev/null || printf 'none')"
    set -- $(ahead_behind_for_path "$path")
    ahead="$1"
    behind="$2"

    blocker="none"
    case "$registration" in
      excluded-local)
        eligibility="excluded"
        blocker="excluded-by-policy"
        ;;
      *)
        if [ "$remote" = "none" ]; then
          blocker="$(append_blocker "$blocker" "no-origin-remote")"
        fi
        if [ "$state" != "clean" ]; then
          blocker="$(append_blocker "$blocker" "dirty-working-tree")"
        fi
        if [ "$target_branch" = "n/a" ]; then
          blocker="$(append_blocker "$blocker" "no-target-branch")"
        elif [ "$current_branch" != "$target_branch" ]; then
          blocker="$(append_blocker "$blocker" "branch-mismatch")"
        fi
        if [ "$ahead" = "-" ] || [ "$behind" = "-" ]; then
          blocker="$(append_blocker "$blocker" "no-upstream")"
        else
          if [ "$ahead" != "0" ]; then
            blocker="$(append_blocker "$blocker" "ahead-of-upstream")"
          fi
          if [ "$behind" != "0" ]; then
            blocker="$(append_blocker "$blocker" "behind-upstream")"
          fi
        fi

        if [ "$blocker" = "none" ]; then
          eligibility="eligible-observed"
        else
          eligibility="blocked"
        fi
        ;;
    esac
  fi

  printf '| `%s` | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |\n' \
    "$(sanitize_cell "$path")" \
    "$(sanitize_cell "$registration")" \
    "$(sanitize_cell "$current_branch")" \
    "$(sanitize_cell "$target_branch")" \
    "$(sanitize_cell "$state")" \
    "$(sanitize_cell "$ahead")" \
    "$(sanitize_cell "$behind")" \
    "$(sanitize_cell "$remote")" \
    "$(sanitize_cell "$gitlink")" \
    "$(sanitize_cell "$bun_membership")" \
    "$(sanitize_cell "$uv_membership")" \
    "$(sanitize_cell "$eligibility")" \
    "$(sanitize_cell "$blocker")"
}

BUN_WORKSPACES="$(list_package_workspaces)"
UV_MEMBERS="$(list_uv_members)"

cat <<'EOF'
# Workspace Trusted Baseline

This report is a live observation assembled from `.gitmodules`, active gitlinks,
root workspace manifests, root policy, and child Git status. It is not a source
of truth and not permission to pin, repair, or mutate child repositories.

| path | registration | branch | target | state | ahead | behind | remote | gitlink | bun | uv | eligibility | blocker |
|------|--------------|--------|--------|-------|-------|--------|--------|---------|-----|----|-------------|---------|
EOF

list_report_paths | while IFS= read -r path; do
  [ -n "$path" ] || continue
  print_row "$path"
done
