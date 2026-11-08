#!/bin/sh
# Root-owned remote-management policy; package/runtime membership is separate.
repository_is_local_only() {
  case "$1" in
    rich) return 0 ;;
    *) return 1 ;;
  esac
}
