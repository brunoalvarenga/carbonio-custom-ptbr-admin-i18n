#!/usr/bin/env bash
set -euo pipefail

MODULE_ID="carbonio-custom-ptbr-admin-i18n"
APP_DIR="${CARBONIO_PTBR_APP_DIR:-/opt/$MODULE_ID}"
TRANSLATION_FILE="$APP_DIR/translations/pt.json"
DATA_DIR="/var/lib/$MODULE_ID"
BACKUP_ROOT="/var/backups/$MODULE_ID"
STATUS_FILE="$DATA_DIR/status.json"

if [ "$(id -u)" != "0" ]; then
  echo "Execute como root." >&2
  exit 1
fi

if [ ! -s "$TRANSLATION_FILE" ]; then
  echo "Arquivo de traducao nao encontrado: $TRANSLATION_FILE" >&2
  exit 1
fi

python3 -m json.tool "$TRANSLATION_FILE" >/dev/null

install -d -m 0755 "$DATA_DIR" "$BACKUP_ROOT"
backup_dir="$BACKUP_ROOT/$(date -u +%Y%m%dT%H%M%SZ)"
install -d -m 0755 "$backup_dir"

targets=(
  "/opt/zextras/admin/iris/i18n"
  "/opt/zextras/admin/iris/src/i18n"
  "/opt/zextras/admin/iris/carbonio-admin-ui/i18n"
  "/opt/zextras/admin/iris/carbonio-admin-ui/src/i18n"
  "/opt/zextras/admin/iris/carbonio-admin-ui/current/i18n"
  "/opt/zextras/admin/iris/carbonio-admin-ui/current/src/i18n"
)

applied=()
for dir in "${targets[@]}"; do
  install -d -m 0755 "$dir"
  target="$dir/pt.json"
  if [ -f "$target" ]; then
    cp --parents "$target" "$backup_dir"/
  fi
  install -m 0644 "$TRANSLATION_FILE" "$target"
  applied+=("$target")
  if [ ! -s "$dir/en.json" ]; then
    printf '{}\n' > "$dir/en.json"
    chmod 0644 "$dir/en.json"
  fi
done

sha="$(sha256sum "$TRANSLATION_FILE" | awk '{print $1}')"
version="$(tr -d '[:space:]' < "$APP_DIR/VERSION")"
applied_json="$(printf '%s\n' "${applied[@]}" | python3 -c 'import json,sys; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))')"

python3 - "$STATUS_FILE" "$MODULE_ID" "$version" "$sha" "$backup_dir" "$applied_json" <<'PY'
import json
import sys
from datetime import datetime, timezone

status_file, module_id, version, sha, backup_dir, applied_json = sys.argv[1:]
data = {
    "module": module_id,
    "version": version,
    "locale": "pt-BR",
    "translation_sha256": sha,
    "last_applied_utc": datetime.now(timezone.utc).isoformat(),
    "backup_dir": backup_dir,
    "applied_files": json.loads(applied_json),
    "result": "ok",
}
with open(status_file, "w", encoding="utf-8") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
PY

chmod 0644 "$STATUS_FILE"
echo "$MODULE_ID repair ok"
