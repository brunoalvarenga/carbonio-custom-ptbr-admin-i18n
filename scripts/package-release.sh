#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="$(tr -d '[:space:]' < "$ROOT/VERSION")"
NAME="carbonio-custom-ptbr-admin-i18n-$VERSION"
OUT="$ROOT/$NAME.zip"

cd "$ROOT"
rm -f "$OUT"
(cd "$ROOT" && find . -type f \
  ! -name 'manifest.sha256' \
  ! -name '*.tar.gz' \
  ! -name '*.zip' \
  ! -path './.git/*' \
  ! -path './__pycache__/*' \
  ! -path './*/__pycache__/*' \
  -print0 | sort -z | xargs -0 shasum -a 256 > manifest.sha256)
zip -qr "$OUT" . \
  -x '*.zip' \
  -x '*.tar.gz' \
  -x '.git/*' \
  -x '*/.git/*' \
  -x '__pycache__/*' \
  -x '*/__pycache__/*' \
  -x 'release-parts/*' \
  -x '__MACOSX/*' \
  -x '*/._*' \
  -x '.DS_Store'
echo "$OUT"
