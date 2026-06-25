#!/bin/sh
#
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
#
# Build API docs with pdoc.
#
# Environment variables:
#   VERSION         Version label for the footer. If unset, derived from git
#                   branch + short commit (e.g. "main@a1b2c3d"). Falls back to
#                   "dev" when git is unavailable. Set explicitly for releases.
#   PDOC_OUT        Output directory (default: /tmp/apidoc).
#   PDOC_LOGO_LINK  URL for the logo link (default: /spdx-python-model/doc/).

set -e

if [ -z "$VERSION" ]; then
    BRANCH=$(git branch --show-current 2>/dev/null)
    [ -z "$BRANCH" ] && BRANCH="${GITHUB_REF_NAME:-}"
    COMMIT=$(git rev-parse --short HEAD 2>/dev/null || true)
    if [ -n "$BRANCH" ] && [ -n "$COMMIT" ]; then
        VERSION="${BRANCH}@${COMMIT}"
    else
        VERSION="dev"
    fi
fi

GENERATED_AT="$(date -u '+%Y-%m-%d %H:%M UTC')"
OUT="${PDOC_OUT:-/tmp/apidoc}"
LOGO_LINK="${PDOC_LOGO_LINK:-/spdx-python-model/doc/}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Embed logo as data URI so it renders correctly on all pages at any depth,
# both locally (file://) and on the hosted site.
LOGO_DATA="data:image/svg+xml;base64,$(base64 < "$REPO_ROOT/www/img/logo.svg" | tr -d '\n')"

pdoc spdx_python_model \
    --logo "$LOGO_DATA" \
    --logo-link "$LOGO_LINK" \
    --footer-text "Generated from spdx-python-model $VERSION at $GENERATED_AT" \
    -o "$OUT"

echo "API docs written to $OUT"
