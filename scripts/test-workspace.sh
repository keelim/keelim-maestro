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

workspace_includes() {
  workspace_path="$1"

  bun --eval "const fs = require('fs'); const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8')); if (!(pkg.workspaces || []).includes('${workspace_path}')) process.exit(1);" >/dev/null 2>&1
}

uv_workspace_includes() {
  workspace_path="$1"

  bun --eval "const fs = require('fs'); const text = fs.readFileSync('pyproject.toml', 'utf8'); const section = text.match(/\\[tool\\.uv\\.workspace\\][\\s\\S]*?(?=\\n\\[|$)/)?.[0] || ''; const members = [...section.matchAll(/\"([^\"]+)\"/g)].map((match) => match[1]); if (!members.includes('${workspace_path}')) process.exit(1);" >/dev/null 2>&1
}

trusted_baseline_report_runs() {
  sh scripts/report-trusted-baseline.sh >/dev/null
}

shared_ui_contract_report_runs() {
  sh scripts/report-shared-ui-contract.sh >/dev/null
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
  run_check "CodeGraph dispatcher script exists in package scripts" package_script_exists "cg"
  run_check "CodeGraph status script exists in package scripts" package_script_exists "cg:status"
  run_check "CodeGraph root-check script exists in package scripts" package_script_exists "cg:root-check"
  run_check "baseline report script exists in package scripts" package_script_exists "report:baseline"
  run_check "shared UI contract report script exists in package scripts" package_script_exists "report:shared-ui"
  run_check "web typecheck script exists" package_script_exists "typecheck:web"
  run_check "web build script exists" package_script_exists "build:web"
  run_check "web test script exists" package_script_exists "test:web"
  run_check "codex app-server dev script exists" package_script_exists "dev:codex-app-server"
  run_check "local automation script exists in package scripts" package_script_exists "automation:local"
}

check_root_files() {
  run_check "root README exists" test -f README.md
  run_check "root .gitignore exists" test -f .gitignore
  run_check "root .gitmodules exists" test -f .gitmodules
  run_check "root CodeGraph dispatcher exists" test -f scripts/codegraph.sh
  run_check "root update-subrepos helper exists" test -f scripts/update-subrepos.sh
  run_check "root trusted-baseline reporter exists" test -f scripts/report-trusted-baseline.sh
  run_check "root trusted-baseline reporter runs" trusted_baseline_report_runs
  run_check "root shared UI contract reporter exists" test -f scripts/report-shared-ui-contract.sh
  run_check "root shared UI contract reporter runs" shared_ui_contract_report_runs
  run_check "root all-web-ui verifier exists" test -f scripts/verify-all-web-ui-integration.sh
  run_check "root keelim-plugin verifier exists" test -f scripts/verify-keelim-plugin-rename.sh
  run_check "root codex app-server helper exists" test -f scripts/codex-app-server.sh
  run_check "root local automation helper exists" test -f scripts/local-automation.sh
  run_check "root knowledge docs README exists" test -f docs/knowledge/README.md
  run_check "root GBrain contract exists" test -f docs/knowledge/gbrain.md
  run_check "root GBrain source targets exist" test -f docs/knowledge/source-targets.md
  run_check "root GBrain operator runbook exists" test -f docs/knowledge/operator-runbook.md
  run_check "root GBrain verification contract exists" test -f docs/knowledge/verification-contract.md
}

check_local_automation_contract() {
  run_check "local automation gbrain usage is documented in helper" file_contains scripts/local-automation.sh "scripts/local-automation.sh verify [all|rich|n8n|agentgateway|gbrain]"
  run_check "local automation standby usage is documented in helper" file_contains scripts/local-automation.sh "scripts/local-automation.sh standby [all|rich|n8n|agentgateway]"
  run_check "local automation keeps agentgateway fixed during standby" file_contains scripts/local-automation.sh "agentgateway is the fixed Kubernetes resource; standby leaves it unchanged."
  run_check "local automation keeps gbrain read-only" file_contains scripts/local-automation.sh "gbrain is read-only from this helper: list, status, and verify only."
  run_check "local automation standby contract is documented" file_contains docs/ops/local-automation-stack.md 'standby` keeps `agentgateway` fixed and unchanged'
  run_check "local automation gbrain contract is documented" file_contains docs/ops/local-automation-stack.md '`gbrain` supports only `list`, `status`, and `verify`'
}

check_autonomous_repo_contract() {
  run_check "root ignores all-web-ui" file_contains .gitignore "/all-web-ui/"
  run_check "root ignores quant" file_contains .gitignore "/quant/"
  run_check "root ignores rich" file_contains .gitignore "/rich/"
  run_check "root ignores youtube" file_contains .gitignore "/youtube/"
  run_check "root ignores archived toto" file_contains .gitignore "/toto/"
  run_check "root workspaces exclude quant" workspace_excludes "quant"
  run_check "root workspaces exclude rich" workspace_excludes "rich"
  run_check "root workspaces exclude top-level youtube" workspace_excludes "youtube"
  run_check "root workspaces include youtube remotion" workspace_includes "youtube/remotion"
  run_check "root workspaces include youtube services" workspace_includes "youtube/services/*"
  run_check "root workspaces include youtube videos" workspace_includes "youtube/videos/*"
  run_check "root workspaces exclude archived toto" workspace_excludes "toto"
  run_check "root uv workspace includes rich" uv_workspace_includes "rich"
  run_check "root uv workspace includes youtube" uv_workspace_includes "youtube"
}

main() {
  print_header
  check_package_contract
  check_root_files
  check_local_automation_contract
  check_autonomous_repo_contract

  if [ "$FAILURES" -ne 0 ]; then
    printf '\nWorkspace contract tests failed (%s issue%s).\n' "$FAILURES" "$( [ "$FAILURES" -eq 1 ] && printf '' || printf 's' )"
    exit 1
  fi

  printf '\nWorkspace contract tests passed.\n'
}

main "$@"
