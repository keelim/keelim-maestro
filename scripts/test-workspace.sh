#!/bin/sh
set -eu

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

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

file_contains() {
  file_path="$1"
  needle="$2"

  grep -F "$needle" "$file_path" >/dev/null 2>&1
}

path_is_git_repo() {
  target="$1"

  [ -d "$target/.git" ] || [ -f "$target/.git" ]
}

package_json_assert() {
  description="$1"
  expression="$2"

  if bun --eval "const fs = require('fs'); const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8')); if (!(${expression})) process.exit(1);" >/dev/null 2>&1; then
    pass "$description"
  else
    fail "$description"
  fi
}

package_script_exists() {
  script_name="$1"

  bun --eval "const fs = require('fs'); const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8')); if (!pkg.scripts || !pkg.scripts['${script_name}']) process.exit(1);" >/dev/null 2>&1
}

workspace_excludes() {
  workspace_path="$1"

  bun --eval "const fs = require('fs'); const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8')); if ((pkg.workspaces || []).includes('${workspace_path}')) process.exit(1);" >/dev/null 2>&1
}

root_does_not_track_path() {
  target="$1"

  ! git ls-files --error-unmatch "$target" >/dev/null 2>&1
}

root_ignores_path() {
  target="$1"

  git check-ignore -q "$target"
}

print_header() {
  printf 'Workspace root: %s\n' "$ROOT"
  printf 'Mode: root contract\n\n'
}

check_package_contract() {
  package_json_assert "root package is private" "pkg.private === true"
  package_json_assert "root packageManager is Bun" "typeof pkg.packageManager === 'string' && pkg.packageManager.startsWith('bun@')"
  package_json_assert "root workspaces is an array" "Array.isArray(pkg.workspaces)"
  package_json_assert "root scripts is an object" "pkg.scripts && typeof pkg.scripts === 'object'"

  run_check "default test script exists" package_script_exists "test"
  run_check "workspace test script exists" package_script_exists "test:workspace"
  run_check "web typecheck script exists" package_script_exists "typecheck:web"
  run_check "web build script exists" package_script_exists "build:web"
  run_check "web test script exists" package_script_exists "test:web"
  run_check "toto verify script exists" package_script_exists "verify:toto"
}

check_root_files() {
  run_check "root README exists" test -f README.md
  run_check "root .gitignore exists" test -f .gitignore
  run_check "root .gitmodules exists" test -f .gitmodules
  run_check "root update-subrepos helper exists" test -f scripts/update-subrepos.sh
  run_check "root all-web-ui verifier exists" test -f scripts/verify-all-web-ui-integration.sh
  run_check "root keelim-plugin verifier exists" test -f scripts/verify-keelim-plugin-rename.sh
}

check_autonomous_repo_contract() {
  run_check "root ignores all-web-ui" file_contains .gitignore "/all-web-ui/"
  run_check "root ignores agent-skill-console" file_contains .gitignore "/agent-skill-console/"
  run_check "root ignores quant" file_contains .gitignore "/quant/"
  run_check "root ignores rich" file_contains .gitignore "/rich/"
  run_check "root workspaces exclude agent-skill-console" workspace_excludes "agent-skill-console"
  run_check "root workspaces exclude quant" workspace_excludes "quant"
  run_check "root workspaces exclude rich" workspace_excludes "rich"

  if [ -e agent-skill-console ]; then
    run_check "agent-skill-console is ignored by root" root_ignores_path "agent-skill-console/"
    run_check "agent-skill-console is not tracked by root" root_does_not_track_path "agent-skill-console"
    run_check "agent-skill-console is its own git repo" path_is_git_repo "agent-skill-console"
  else
    pass "agent-skill-console optional child repo is absent"
  fi
}

main() {
  print_header
  check_package_contract
  check_root_files
  check_autonomous_repo_contract

  if [ "$FAILURES" -ne 0 ]; then
    printf '\nWorkspace contract tests failed (%s issue%s).\n' "$FAILURES" "$( [ "$FAILURES" -eq 1 ] && printf '' || printf 's' )"
    exit 1
  fi

  printf '\nWorkspace contract tests passed.\n'
}

main "$@"
