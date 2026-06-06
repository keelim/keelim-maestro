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
  scripts/local-automation.sh standby [all|rich|n8n|agentgateway]
  scripts/local-automation.sh start <rich|n8n|agentgateway>
  scripts/local-automation.sh stop <rich|n8n|agentgateway>

Purpose:
  Keep root-level local automation commands discoverable while delegating
  runtime ownership to rich, youtube, and tools/agentgateway.
  agentgateway is the fixed Kubernetes resource; rich and n8n are on-demand.
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

scale_deployment_to_zero() {
  namespace="$1"
  deployment="$2"

  KUBECTL="$(kubectl_bin)"
  if [ -z "$KUBECTL" ]; then
    printf '[skip] kubectl not found in PATH or /usr/local/bin/kubectl\n'
    mark_failure
    return 0
  fi

  if ! "$KUBECTL" get namespace "$namespace" >/dev/null 2>&1; then
    printf '[info] namespace/%s is not present; deployment/%s is already idle\n' "$namespace" "$deployment"
    return 0
  fi

  if ! "$KUBECTL" -n "$namespace" get deployment "$deployment" >/dev/null 2>&1; then
    printf '[info] deployment/%s is not present in namespace/%s\n' "$deployment" "$namespace"
    return 0
  fi

  run_kubectl -n "$namespace" scale deployment "$deployment" --replicas=0
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
  info "Stop:   scripts/local-automation.sh standby rich"
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
  info "Role:   fixed local Kubernetes resource; keep it up for MCP access"
  info "Start:  cd tools/agentgateway && bash scripts/start-k8s-gateway.sh"
  info "Verify: cd tools/agentgateway && AGENTGATEWAY_URL=http://127.0.0.1:3000 bash scripts/verify-k8s-gateway.sh"
  info "Stop:   cd tools/agentgateway && bash scripts/stop-k8s-gateway.sh --apply"
  info "MCP:    Codex/Claude -> http://127.0.0.1:3000/mcp -> agentgateway -> Supabase/Lazyweb/Stitch"
  info "Files:  tools/agentgateway/scripts/, tools/agentgateway/k8s/"
}

status_rich() {
  section "rich status"
  run_kubectl -n rich-local get deploy,svc,pod
  run_lsof_port 8000
  run_lsof_port 3001
}

status_n8n() {
  section "n8n status"
  run_kubectl -n automation get deploy,svc,pvc,pod
  run_lsof_port 5678
}

status_agentgateway() {
  section "agentgateway status"
  run_kubectl -n agentgateway-local get deployment/agentgateway-local service/agentgateway-local
  run_kubectl -n agentgateway-local get pod -l app.kubernetes.io/name=agentgateway-local
  run_lsof_port 3000
  run_lsof_port 15000
}

verify_rich() {
  section "rich verify"
  run_kubectl -n rich-local get deploy,svc,pod
  run_cmd "curl -fsS http://127.0.0.1:8000/healthz" curl -fsS http://127.0.0.1:8000/healthz
  info "Admin UI: http://127.0.0.1:3001/admin"
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
    AGENTGATEWAY_URL=http://127.0.0.1:3000 bash scripts/verify-k8s-gateway.sh
  ) || mark_failure
}

rich_skaffold_pids() {
  if ! command -v ps >/dev/null 2>&1; then
    return 0
  fi

  ps -axo pid=,command= | while IFS= read -r line; do
    case "$line" in
      *"skaffold dev"*"$ROOT_DIR/rich/skaffold.yaml"*|*"skaffold dev"*"/rich/skaffold.yaml"*)
        pid="$(printf '%s\n' "$line" | awk '{print $1}')"
        if [ -n "$pid" ] && [ "$pid" != "$$" ]; then
          printf '%s\n' "$pid"
        fi
        ;;
    esac
  done | sort -u
}

stop_rich_skaffold_loops() {
  pids="$(rich_skaffold_pids || true)"

  if [ -z "$pids" ]; then
    info "[info] no rich Skaffold dev loop found"
    return 0
  fi

  for pid in $pids; do
    command="$(ps -p "$pid" -o command= 2>/dev/null || true)"
    if kill "$pid" 2>/dev/null; then
      printf 'stopped rich skaffold pid=%s command=%s\n' "$pid" "$command"
    else
      printf 'failed to stop rich skaffold pid=%s command=%s\n' "$pid" "$command" >&2
      mark_failure
    fi
  done

  sleep 2
}

standby_rich() {
  section "rich standby"
  stop_rich_skaffold_loops
  scale_deployment_to_zero rich-local rich-backend
  scale_deployment_to_zero rich-local rich-frontend
}

standby_n8n() {
  section "n8n standby"
  scale_deployment_to_zero automation n8n
}

standby_agentgateway() {
  section "agentgateway fixed"
  info "agentgateway is the fixed Kubernetes resource; standby leaves it unchanged."
  info "Use scripts/local-automation.sh verify agentgateway to check it, or start agentgateway if it is intentionally down."
}

standby_runtime() {
  case "$TARGET" in
    all)
      standby_rich
      standby_n8n
      standby_agentgateway
      ;;
    rich)
      standby_rich
      ;;
    n8n)
      standby_n8n
      ;;
    agentgateway)
      standby_agentgateway
      ;;
    *)
      print_usage
      exit 1
      ;;
  esac
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
      exec bash scripts/start-k8s-gateway.sh
      ;;
  esac
}

stop_runtime() {
  require_single_runtime

  case "$TARGET" in
    rich)
      standby_rich
      ;;
    n8n)
      standby_n8n
      ;;
    agentgateway)
      section "agentgateway stop"
      (
        cd tools/agentgateway
        bash scripts/stop-k8s-gateway.sh --apply
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
  standby)
    standby_runtime
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
