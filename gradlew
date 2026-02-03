#!/usr/bin/env bash
set -euo pipefail

if ! command -v gradle >/dev/null 2>&1; then
  echo "Gradle is required but not installed." >&2
  exit 1
fi

exec gradle "$@"
