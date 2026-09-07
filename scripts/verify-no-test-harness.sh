#!/usr/bin/env bash
# Fail if built HTML still contains CI test-harness markers (TD-001).
set -euo pipefail

DIST="${1:-dist}"
PATTERN='#!test|#{{|#}}|//!test|//{{|//}}'

if [[ ! -d "$DIST" ]]; then
  echo "verify-no-test-harness: dist directory not found: $DIST" >&2
  exit 1
fi

mapfile -t matches < <(grep -R -l -E "$PATTERN" "$DIST" --include='*.html' 2>/dev/null || true)

if ((${#matches[@]} > 0)); then
  echo "verify-no-test-harness: harness markers found in ${#matches[@]} HTML file(s):" >&2
  printf '  %s\n' "${matches[@]}" >&2
  exit 1
fi

echo "verify-no-test-harness: OK (no harness markers in $DIST)"
