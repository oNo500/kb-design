#!/bin/sh
set -eu
cd "$(dirname "$0")"
exec uv run --package kb-vocab python sync-current.py "$@"
