#!/usr/bin/env bash
set -Eeuo pipefail

CACHE_PATH=${CACHE_PATH:-"/tmp/nixcache"}

banner() {
  echo "========================================================"
  echo "  $*"
  echo "========================================================"
}

# banner "List what we start with"
# ls -alh "${CACHE_PATH}"

banner "Copy time"
nix copy --from "file://${CACHE_PATH}" --no-check-sigs --all
