#!/bin/bash
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

npm install

echo "export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers" >> "$CLAUDE_ENV_FILE"
