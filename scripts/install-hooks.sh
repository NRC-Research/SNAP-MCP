#!/usr/bin/env bash
# Points this clone's git hooks at .githooks/ and checks that the redaction
# pattern file exists.
#
# Run once per clone:  scripts/install-hooks.sh
#
# Hooks are per-clone and never travel with a push, so every machine that
# commits to this repo needs this. The CI check in
# .github/workflows/redaction-check.yml is the backstop for machines that skip
# it, and for merges made in the web UI where no hook can run.

set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"

chmod +x .githooks/*
git config core.hooksPath .githooks
echo "Hooks enabled: core.hooksPath -> .githooks"

PATTERNS="${SNAP_MCP_PATTERNS:-$HOME/.config/snap-mcp/redaction-patterns.txt}"
if [ -s "$PATTERNS" ]; then
  echo "Pattern file found: $PATTERNS ($(wc -l < "$PATTERNS" | tr -d ' ') patterns)"
else
  echo ""
  echo "WARNING: no pattern file at $PATTERNS"
  echo "  The pre-commit redaction check will refuse to run without it."
  echo "  Create it (one pattern per line, chmod 600) or set SNAP_MCP_PATTERNS."
  echo "  It must live OUTSIDE this repo -- the denylist is itself sensitive."
fi
