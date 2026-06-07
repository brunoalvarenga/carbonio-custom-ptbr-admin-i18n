#!/usr/bin/env bash
set -euo pipefail

MODULE_ID="carbonio-custom-ptbr-admin-i18n"
INSTALL_DIR="/opt/$MODULE_ID"
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ "$(id -u)" != "0" ]; then
  echo "Execute como root." >&2
  exit 1
fi

install -d -m 0755 "$INSTALL_DIR"
install -d -m 0755 "/var/lib/$MODULE_ID" "/var/backups/$MODULE_ID"
find "$INSTALL_DIR" -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +
cp -a "$SRC_DIR"/. "$INSTALL_DIR"/
find "$INSTALL_DIR" \( -name '._*' -o -name '.DS_Store' -o -name "$MODULE_ID-*.zip" \) -type f -delete
chmod 0755 "$INSTALL_DIR/install.sh" "$INSTALL_DIR/repair.sh" "$INSTALL_DIR/uninstall.sh"
chmod 0755 "$INSTALL_DIR/scripts/"*.sh "$INSTALL_DIR/scripts/"*.py 2>/dev/null || true

install -m 0644 "$SRC_DIR/systemd/$MODULE_ID.service" "/etc/systemd/system/$MODULE_ID.service"
install -m 0644 "$SRC_DIR/systemd/$MODULE_ID-guard.timer" "/etc/systemd/system/$MODULE_ID-guard.timer"

systemctl daemon-reload
bash "$INSTALL_DIR/repair.sh"
systemctl enable "$MODULE_ID.service" >/dev/null 2>&1 || true
systemctl enable --now "$MODULE_ID-guard.timer" >/dev/null 2>&1 || true

if [ -x /opt/zextras/common/sbin/nginx ]; then
  /opt/zextras/common/sbin/nginx -t -c /opt/zextras/conf/nginx.conf
fi
systemctl reload carbonio-nginx 2>/dev/null || systemctl reload nginx 2>/dev/null || true

echo "$MODULE_ID instalado."
echo "Locale aplicado: pt-BR"
