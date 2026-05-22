#!/bin/sh
set -eu

usage() {
  cat <<'USAGE'
Run the Codex app-server from the keelim-maestro workspace root.

Usage:
  sh scripts/codex-app-server.sh [codex app-server options]

Environment:
  CODEX_APP_SERVER_LISTEN  Transport endpoint. Defaults to ws://127.0.0.1:7331
  CODEX_BIN                Codex executable. Defaults to codex

Examples:
  sh scripts/codex-app-server.sh
  CODEX_APP_SERVER_LISTEN=unix:///tmp/codex-app.sock sh scripts/codex-app-server.sh
  codex --remote ws://127.0.0.1:7331
USAGE
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

CODEX_BIN="${CODEX_BIN:-codex}"
LISTEN="${CODEX_APP_SERVER_LISTEN:-ws://127.0.0.1:7331}"

if ! command -v "$CODEX_BIN" >/dev/null 2>&1; then
  printf 'Codex executable not found: %s\n' "$CODEX_BIN" >&2
  printf 'Set CODEX_BIN=/path/to/codex or install Codex first.\n' >&2
  exit 127
fi

HAS_WS_AUTH=0
for arg in "$@"; do
  case "$arg" in
    --ws-auth|--ws-auth=*) HAS_WS_AUTH=1 ;;
  esac
done

case "$LISTEN" in
  ws://127.0.0.1:*|ws://localhost:*|ws://[::1]:*|stdio://|unix://*)
    ;;
  ws://*)
    if [ "$HAS_WS_AUTH" -ne 1 ]; then
      printf 'Refusing non-loopback websocket listener without --ws-auth.\n' >&2
      printf 'Use CODEX_APP_SERVER_LISTEN=ws://127.0.0.1:7331 for local-only access,\n' >&2
      printf 'or pass Codex websocket auth options explicitly.\n' >&2
      exit 2
    fi
    ;;
esac

printf 'Starting Codex app-server\n'
printf 'Workspace: %s\n' "$ROOT"
printf 'Listen:    %s\n' "$LISTEN"

case "$LISTEN" in
  ws://127.0.0.1:*|ws://localhost:*|ws://[::1]:*)
    printf 'Connect:   codex --remote %s\n' "$LISTEN"
    ;;
esac

exec "$CODEX_BIN" app-server --listen "$LISTEN" "$@"
