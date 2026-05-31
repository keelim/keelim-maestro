#!/bin/sh
set -eu

ROOT_DIR="$(git rev-parse --show-toplevel)"
cd "$ROOT_DIR"

ACTION="${1:-status}"
TARGET="${2:-all}"
FAILURES=0

print_usage() {
  cat <<'EOF'
Usage:
  scripts/local-automation.sh list [all|rich|n8n|agentgateway]
  scripts/local-automation.sh status [all|rich|n8n|agentgateway]
  scripts/local-automation.sh verify [all|rich|n8n|agentgateway]
  scripts/local-automation.sh start <rich|n8n|agentgateway>
  scripts/local-automation.sh stop <rich|n8n|agentgateway>

Purpose:
  Keep root-level local automation commands discoverable while delegating
  runtime ownership to rich, youtube, and tools/agentgateway.
EOF
}

section() {
  printf '\n## %s\n' "$1"
}

info() {
  printf '%s\n' "$1"
}

mark_failure() {
  FAILURES=$((FAILURES + 1))
}

run_cmd() {
  description="$1"
  shift

  printf '+ %s\n' "$description"
  if "$@"; then
    return 0
  fi

  mark_failure
  return 0
}

kubectl_bin() {
  if command -v kubectl >/dev/null 2>&1; then
    command -v kubectl
    return 0
  fi

  if [ -x /usr/local/bin/kubectl ]; then
    printf '%s\n' /usr/local/bin/kubectl
    return 0
  fi

  printf '\n'
}

run_kubectl() {
  KUBECTL="$(kubectl_bin)"
  if [ -z "$KUBECTL" ]; then
    printf '[skip] kubectl not found in PATH or /usr/local/bin/kubectl\n'
    mark_failure
    return 0
  fi

  "$KUBECTL" "$@" || mark_failure
}

run_lsof_port() {
  port="$1"

  if ! command -v lsof >/dev/null 2>&1; then
    printf '[skip] lsof not found; cannot inspect port %s\n' "$port"
    return 0
  fi

  if lsof -nP -iTCP:"$port" -sTCP:LISTEN; then
    return 0
  fi

  printf '[info] no listener on TCP port %s\n' "$port"
}

targets_for_action() {
  case "$TARGET" in
    all)
      printf '%s\n' rich n8n agentgateway
      ;;
    rich|n8n|agentgateway)
      printf '%s\n' "$TARGET"
      ;;
    *)
      print_usage
      exit 1
      ;;
  esac
}

require_single_runtime() {
  if [ "$TARGET" = "all" ]; then
    printf 'Choose one runtime for %s: rich, n8n, or agentgateway.\n' "$ACTION"
    exit 1
  fi
}

list_rich() {
  section "rich local Kubernetes"
  info "Owner repo: rich"
  info "Start:  cd rich && sh run-k8s-dev.sh"
  info "Verify: scripts/local-automation.sh verify rich"
  info "Stop:   interrupt the foreground Skaffold loop that started rich"
  info "Files:  rich/run-k8s-dev.sh, rich/skaffold.yaml, rich/k8s/local/"
}

list_n8n() {
  section "youtube n8n Kubernetes"
  info "Owner repo: /Users/keelim/Desktop/youtube"
  info "Start:  cd /Users/keelim/Desktop/youtube/ops/n8n-k8s && kubectl apply -k ."
  info "Verify: scripts/local-automation.sh verify n8n"
  info "Stop:   kubectl -n automation scale deployment/n8n --replicas=0"
  info "Files:  /Users/keelim/Desktop/youtube/ops/n8n-k8s/"
}

list_agentgateway() {
  section "agentgateway MCP Kubernetes"
  info "Owner repo: tools/agentgateway"
  info "Start:  cd tools/agentgateway && sh scripts/start-k8s-gateway.sh"
  info "Verify: cd tools/agentgateway && AGENTGATEWAY_URL=http://127.0.0.1:3000 sh scripts/verify-k8s-gateway.sh"
  info "Stop:   cd tools/agentgateway && sh scripts/stop-k8s-gateway.sh --apply"
  info "Files:  tools/agentgateway/scripts/, tools/agentgateway/k8s/"
}

status_rich() {
  section "rich status"
  run_kubectl -n rich-local get deploy,svc,pod
  run_lsof_port 8000
  run_lsof_port 3000
}

status_n8n() {
  section "n8n status"
  run_kubectl -n automation get deploy,svc,pvc,pod
  run_lsof_port 5678
}

status_agentgateway() {
  section "agentgateway status"
  run_kubectl -n agentgateway-local get deploy,svc,pod
  run_lsof_port 3000
  run_lsof_port 15000
}

verify_rich() {
  section "rich verify"
  run_kubectl -n rich-local get deploy,svc,pod
  run_cmd "curl -fsS http://127.0.0.1:8000/healthz" curl -fsS http://127.0.0.1:8000/healthz
  info "Admin UI: http://127.0.0.1:3000/admin"
}

verify_n8n() {
  section "n8n verify"
  run_kubectl -n automation get deploy,svc,pvc,pod
  run_cmd "curl -fsSL --max-time 10 http://localhost:5678" curl -fsSL --max-time 10 http://localhost:5678
  run_kubectl -n automation exec deploy/n8n -c n8n -- test -d /data/easy-release-note/renders
  run_kubectl -n automation exec deploy/n8n -c task-runners -- test -d /data/easy-release-note/renders
}

verify_agentgateway() {
  section "agentgateway verify"
  if [ ! -f tools/agentgateway/scripts/verify-k8s-gateway.sh ]; then
    printf '[fail] tools/agentgateway/scripts/verify-k8s-gateway.sh missing\n'
    mark_failure
    return 0
  fi

  (
    cd tools/agentgateway
    AGENTGATEWAY_URL=http://127.0.0.1:3000 sh scripts/verify-k8s-gateway.sh
  ) || mark_failure
}

start_runtime() {
  require_single_runtime

  case "$TARGET" in
    rich)
      cd rich
      exec sh run-k8s-dev.sh
      ;;
    n8n)
      cd /Users/keelim/Desktop/youtube/ops/n8n-k8s
      KUBECTL="$(kubectl_bin)"
      if [ -z "$KUBECTL" ]; then
        printf 'kubectl not found in PATH or /usr/local/bin/kubectl\n'
        exit 1
      fi
      exec "$KUBECTL" apply -k .
      ;;
    agentgateway)
      cd tools/agentgateway
      exec sh scripts/start-k8s-gateway.sh
      ;;
  esac
}

stop_runtime() {
  require_single_runtime

  case "$TARGET" in
    rich)
      section "rich stop"
      info "No root stop command is defined for rich."
      info "Interrupt the foreground Skaffold loop that started rich so it can clean up its own dev resources."
      ;;
    n8n)
      section "n8n stop"
      run_kubectl -n automation scale deployment/n8n --replicas=0
      ;;
    agentgateway)
      section "agentgateway stop"
      (
        cd tools/agentgateway
        sh scripts/stop-k8s-gateway.sh --apply
      ) || mark_failure
      ;;
  esac
}

run_for_targets() {
  for runtime in $(targets_for_action); do
    case "$ACTION:$runtime" in
      list:rich) list_rich ;;
      list:n8n) list_n8n ;;
      list:agentgateway) list_agentgateway ;;
      status:rich) status_rich ;;
      status:n8n) status_n8n ;;
      status:agentgateway) status_agentgateway ;;
      verify:rich) verify_rich ;;
      verify:n8n) verify_n8n ;;
      verify:agentgateway) verify_agentgateway ;;
      *)
        print_usage
        exit 1
        ;;
    esac
  done
}

case "$ACTION" in
  list|status|verify)
    run_for_targets
    ;;
  start)
    start_runtime
    ;;
  stop)
    stop_runtime
    ;;
  -h|--help|help)
    print_usage
    ;;
  *)
    print_usage
    exit 1
    ;;
esac

if [ "$FAILURES" -ne 0 ]; then
  printf '\nCompleted with %s failure(s).\n' "$FAILURES"
  exit 1
fi
