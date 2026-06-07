#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="$(tr -d '[:space:]' < "$ROOT/VERSION")"
NAME="carbonio-custom-ptbr-admin-i18n-$VERSION"
OUT_DIR="$ROOT/build/xcarbonio"
OUT="$OUT_DIR/$NAME.zip"

cd "$ROOT"
rm -f "$ROOT"/carbonio-custom-ptbr-admin-i18n-*.zip
rm -rf "$OUT_DIR"
install -d -m 0755 "$OUT_DIR"
(cd "$ROOT" && find . -type f \
  ! -name 'manifest.sha256' \
  ! -name '*.tar.gz' \
  ! -name '*.zip' \
  ! -path './.git/*' \
  ! -path './build/*' \
  ! -path './release-parts/*' \
  ! -path './__pycache__/*' \
  ! -path './*/__pycache__/*' \
  -print0 | sort -z | xargs -0 shasum -a 256 > manifest.sha256)
zip -qr "$OUT" . \
  -x '*.zip' \
  -x '*.tar.gz' \
  -x '.git/*' \
  -x '*/.git/*' \
  -x 'build/*' \
  -x '*/build/*' \
  -x '__pycache__/*' \
  -x '*/__pycache__/*' \
  -x 'release-parts/*' \
  -x '__MACOSX/*' \
  -x '*/._*' \
  -x '.DS_Store'
echo "$OUT"
