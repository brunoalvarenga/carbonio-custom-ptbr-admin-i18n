#!/usr/bin/env bash
set -euo pipefail

MODULE_ID="carbonio-custom-ptbr-admin-i18n"
BACKUP_ROOT="/var/backups/$MODULE_ID"

if [ "$(id -u)" != "0" ]; then
  echo "Execute como root." >&2
  exit 1
fi

systemctl disable --now "$MODULE_ID-guard.timer" >/dev/null 2>&1 || true
systemctl disable "$MODULE_ID.service" >/dev/null 2>&1 || true
rm -f "/etc/systemd/system/$MODULE_ID.service" "/etc/systemd/system/$MODULE_ID-guard.timer"
systemctl daemon-reload

latest=""
if [ -d "$BACKUP_ROOT" ]; then
  latest="$(find "$BACKUP_ROOT" -mindepth 1 -maxdepth 1 -type d | sort | tail -n 1)"
fi

if [ -n "$latest" ] && [ -d "$latest/opt" ]; then
  (cd "$latest" && find opt -type f -print0 | while IFS= read -r -d '' file; do
    install -d -m 0755 "/$(dirname "$file")"
    install -m 0644 "$file" "/$file"
  done)
  echo "Backup restaurado: $latest"
else
  echo "Nenhum backup encontrado para restaurar."
fi

systemctl reload carbonio-nginx 2>/dev/null || systemctl reload nginx 2>/dev/null || true
echo "$MODULE_ID removido."
