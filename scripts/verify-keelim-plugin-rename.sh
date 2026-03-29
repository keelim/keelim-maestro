#!/bin/sh
set -eu

ROOT_DIR="$(git rev-parse --show-toplevel)"
COMMON_GIT_DIR="$(git rev-parse --git-common-dir)"
cd "$ROOT_DIR"

failures=0

pass() {
  printf 'PASS: %s\n' "$1"
}

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  failures=$((failures + 1))
}

check_file_contains() {
  file="$1"
  needle="$2"
  label="$3"

  if [ -f "$file" ] && grep -Fq "$needle" "$file"; then
    pass "$label"
  else
    fail "$label"
  fi
}

check_file_absent() {
  file="$1"
  needle="$2"
  label="$3"

  if [ -f "$file" ] && ! grep -Fq "$needle" "$file"; then
    pass "$label"
  else
    fail "$label"
  fi
}

MODULE_DIR="$COMMON_GIT_DIR/modules/keelim-plugin"
MODULE_CONFIG="$MODULE_DIR/config"
CHILD_README="keelim-plugin/README.md"
CHILD_README_TEXT=''
GITLINKS="$(git ls-files --stage | grep '^160000 ' || true)"
SUBMODULE_STATUS="$(git submodule status 2>/dev/null || true)"
ROOT_SUBMODULE_CONFIG="$(git config --file "$COMMON_GIT_DIR/config" --get-regexp '^submodule\..*' 2>/dev/null || true)"

check_file_contains .gitmodules '[submodule "keelim-plugin"]' '.gitmodules renames the submodule section'
check_file_contains .gitmodules 'path = keelim-plugin' '.gitmodules points the submodule path at keelim-plugin'
check_file_contains .gitmodules 'url = https://github.com/keelim/keelim-plugin.git' '.gitmodules points the submodule URL at keelim-plugin'
check_file_contains .gitmodules 'branch = main' '.gitmodules keeps the tracked branch on main'
check_file_absent .gitmodules 'keelim-skill' '.gitmodules removes keelim-skill references'

check_file_contains README.md 'keelim-plugin' 'root README mentions keelim-plugin'
check_file_absent README.md 'keelim-skill' 'root README removes keelim-skill references'

if printf '%s' "$GITLINKS" | grep -Fq 'keelim-plugin'; then
  pass 'git index pins a keelim-plugin gitlink'
else
  printf 'DEBUG[gitlinks]: %s\n' "$GITLINKS" >&2
  fail 'git index pins a keelim-plugin gitlink'
fi

if ! printf '%s' "$GITLINKS" | grep -Fq 'keelim-skill'; then
  pass 'git index no longer pins keelim-skill'
else
  printf 'DEBUG[gitlinks]: %s\n' "$GITLINKS" >&2
  fail 'git index no longer pins keelim-skill'
fi

if printf '%s' "$SUBMODULE_STATUS" | grep -Fq ' keelim-plugin'; then
  pass 'git submodule status lists keelim-plugin'
else
  printf 'DEBUG[submodule-status]: %s\n' "$SUBMODULE_STATUS" >&2
  fail 'git submodule status lists keelim-plugin'
fi

if ! printf '%s' "$SUBMODULE_STATUS" | grep -Fq 'keelim-skill'; then
  pass 'git submodule status removes keelim-skill'
else
  printf 'DEBUG[submodule-status]: %s\n' "$SUBMODULE_STATUS" >&2
  fail 'git submodule status removes keelim-skill'
fi

if printf '%s' "$ROOT_SUBMODULE_CONFIG" | grep -Fq 'submodule.keelim-plugin.url https://github.com/keelim/keelim-plugin.git'; then
  pass 'root git config uses renamed submodule URL'
else
  printf 'DEBUG[root-submodule-config]: %s\n' "$ROOT_SUBMODULE_CONFIG" >&2
  fail 'root git config uses renamed submodule URL'
fi

if ! printf '%s' "$ROOT_SUBMODULE_CONFIG" | grep -Fq 'submodule.keelim-skill'; then
  pass 'root git config removes submodule.keelim-skill'
else
  printf 'DEBUG[root-submodule-config]: %s\n' "$ROOT_SUBMODULE_CONFIG" >&2
  fail 'root git config removes submodule.keelim-skill'
fi

if [ -f 'keelim-plugin/.git' ]; then
  check_file_contains 'keelim-plugin/.git' 'gitdir: ../.git/modules/keelim-plugin' 'submodule gitdir points at .git/modules/keelim-plugin'
else
  fail 'submodule gitdir file exists at keelim-plugin/.git'
fi

if [ -f "$MODULE_CONFIG" ]; then
  check_file_contains "$MODULE_CONFIG" 'worktree = ../../../keelim-plugin' 'module config points its worktree at ../../../keelim-plugin'
  check_file_contains "$MODULE_CONFIG" 'url = https://github.com/keelim/keelim-plugin.git' 'module config points origin at keelim-plugin.git'
else
  fail 'module config exists at .git/modules/keelim-plugin/config'
fi

if [ -f "$CHILD_README" ]; then
  CHILD_README_TEXT="$(cat "$CHILD_README")"
elif [ -d "$MODULE_DIR" ]; then
  CHILD_README_TEXT="$(git --git-dir="$MODULE_DIR" show HEAD:README.md 2>/dev/null || true)"
fi

if [ -n "$CHILD_README_TEXT" ]; then
  if printf '%s' "$CHILD_README_TEXT" | grep -Fq '# keelim-plugin'; then
    pass 'child README title uses keelim-plugin'
  else
    fail 'child README title uses keelim-plugin'
  fi

  if printf '%s' "$CHILD_README_TEXT" | grep -Fq 'npx skills add keelim/keelim-plugin'; then
    pass 'child README install command uses keelim/keelim-plugin'
  else
    fail 'child README install command uses keelim/keelim-plugin'
  fi

  if printf '%s' "$CHILD_README_TEXT" | grep -Fq 'https://github.com/keelim/keelim-plugin'; then
    pass 'child README GitHub URL uses keelim-plugin'
  else
    fail 'child README GitHub URL uses keelim-plugin'
  fi

  if printf '%s' "$CHILD_README_TEXT" | grep -Fq '/keelim-plugin/skills/tech-post-maker'; then
    pass 'child README manual path example uses keelim-plugin'
  else
    fail 'child README manual path example uses keelim-plugin'
  fi

  if ! printf '%s' "$CHILD_README_TEXT" | grep -Fq 'keelim-skill'; then
    pass 'child README removes keelim-skill references'
  else
    fail 'child README removes keelim-skill references'
  fi
else
  fail 'child README is available for verification'
fi

SUBREPO_STATUS="$(./scripts/update-subrepos.sh status 2>/dev/null || true)"
if printf '%s' "$SUBREPO_STATUS" | grep -Eq '^keelim-plugin[[:space:]].*target=main'; then
  pass 'update-subrepos status reports keelim-plugin with target=main'
else
  printf 'DEBUG[update-subrepos]: %s\n' "$SUBREPO_STATUS" >&2
  fail 'update-subrepos status reports keelim-plugin with target=main'
fi

if [ "$failures" -gt 0 ]; then
  printf '\nVerification failed with %s issue(s).\n' "$failures" >&2
  exit 1
fi

printf '\nVerification passed.\n'
