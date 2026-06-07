#!/usr/bin/env bash
set -euo pipefail

MODULE_ID="carbonio-custom-ptbr-admin-i18n"
APP_DIR="${CARBONIO_PTBR_APP_DIR:-/opt/$MODULE_ID}"
TRANSLATION_FILE="$APP_DIR/translations/pt.json"
DATA_DIR="/var/lib/$MODULE_ID"
BACKUP_ROOT="/var/backups/$MODULE_ID"
STATUS_FILE="$DATA_DIR/status.json"
NGINX_PATCH_MARKER="carbonio-custom-ptbr-admin-i18n"
HTML_PATCH_MARKER="carbonio-custom-ptbr-admin-i18n-visual"
VISUAL_ASSET_SRC="$APP_DIR/assets/ptbr-visual-i18n.js"
VISUAL_ASSET_REL="custom-ptbr/ptbr-visual-i18n.js"

if [ "$(id -u)" != "0" ]; then
  echo "Execute como root." >&2
  exit 1
fi

if [ ! -s "$TRANSLATION_FILE" ]; then
  echo "Arquivo de traducao nao encontrado: $TRANSLATION_FILE" >&2
  exit 1
fi

python3 -m json.tool "$TRANSLATION_FILE" >/dev/null
sha="$(sha256sum "$TRANSLATION_FILE" | awk '{print $1}')"

install -d -m 0755 "$DATA_DIR" "$BACKUP_ROOT"
backup_dir="$BACKUP_ROOT/$(date -u +%Y%m%dT%H%M%SZ)"
if [ -e "$backup_dir" ]; then
  backup_dir="$BACKUP_ROOT/$(date -u +%Y%m%dT%H%M%SZ)-$$"
fi
install -d -m 0755 "$backup_dir"

patch_nginx_admin_i18n_route() {
  local file="$1"
  if [ ! -f "$file" ]; then
    return 0
  fi
  cp --parents "$file" "$backup_dir"/
  python3 - "$file" "$NGINX_PATCH_MARKER" <<'PY'
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
marker = sys.argv[2]
text = path.read_text(encoding="utf-8")
text = re.sub(
    rf"\n?[ \t]*# BEGIN {re.escape(marker)}\n.*?# END {re.escape(marker)}\n?",
    "\n",
    text,
    flags=re.S,
)
lines = text.splitlines(keepends=True)
out = []
inserted = 0
for line in lines:
    match = re.match(r"^(\s*)location /carbonioAdmin\b", line)
    if match:
        indent = match.group(1)
        out.append(f"{indent}# BEGIN {marker}\n")
        out.append(f"{indent}location ^~ /carbonioAdmin/src/i18n/ {{\n")
        out.append(f"{indent}    add_header Cache-Control \"no-cache,must-revalidate,no-transform,max-age=604800\";\n")
        out.append(f"{indent}    alias /opt/zextras/admin/iris/src/i18n/;\n")
        out.append(f"{indent}}}\n")
        out.append(f"{indent}# END {marker}\n\n")
        inserted += 1
    out.append(line)
if inserted:
    path.write_text("".join(out), encoding="utf-8")
PY
}

patch_admin_html_visual_i18n() {
  local file="$1"
  local asset_url="$2"
  if [ ! -f "$file" ]; then
    return 0
  fi
  cp --parents "$file" "$backup_dir"/
  python3 - "$file" "$HTML_PATCH_MARKER" "$asset_url" <<'PY'
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
marker = sys.argv[2]
asset_url = sys.argv[3]
text = path.read_text(encoding="utf-8")
text = re.sub(
    rf"\n?[ \t]*<!-- BEGIN {re.escape(marker)} -->\n.*?<!-- END {re.escape(marker)} -->\n?",
    "\n",
    text,
    flags=re.S,
)
block = (
    f"    <!-- BEGIN {marker} -->\n"
    f"    <script defer src=\"{asset_url}\"></script>\n"
    f"    <!-- END {marker} -->\n"
)
if "</body>" in text:
    text = text.replace("  </body>", block + "  </body>", 1)
else:
    text = text + "\n" + block
path.write_text(text, encoding="utf-8")
PY
}

targets=(
  "/opt/zextras/admin/iris/i18n"
  "/opt/zextras/admin/iris/src/i18n"
  "/opt/zextras/admin/iris/carbonio-admin-ui/i18n"
  "/opt/zextras/admin/iris/carbonio-admin-ui/src/i18n"
  "/opt/zextras/admin/iris/carbonio-admin-ui/current/i18n"
  "/opt/zextras/admin/iris/carbonio-admin-ui/current/src/i18n"
)

nginx_files=(
  "/opt/zextras/conf/nginx/templates/nginx.conf.web.carbonio.admin.template"
  "/opt/zextras/conf/nginx/templates/nginx.conf.web.carbonio.admin.default.template"
  "/opt/zextras/conf/nginx/includes/nginx.conf.web.carbonio.admin"
  "/opt/zextras/conf/nginx/includes/nginx.conf.web.carbonio.admin.default"
)

admin_ui_roots=(
  "/opt/zextras/admin/iris/carbonio-admin-ui"
  "/opt/zextras/admin/iris/carbonio-admin-ui/current"
)

admin_html_files=(
  "/opt/zextras/admin/iris/carbonio-admin-ui/index.html"
  "/opt/zextras/admin/iris/carbonio-admin-ui/current/index.html"
)

locale_files=("pt.json" "pt_BR.json" "pt-BR.json")
applied=()
updated=()
skipped=()
for dir in "${targets[@]}"; do
  install -d -m 0755 "$dir"
  for locale_file in "${locale_files[@]}"; do
    target="$dir/$locale_file"
    if [ -f "$target" ]; then
      target_sha="$(sha256sum "$target" | awk '{print $1}')"
      if [ "$target_sha" = "$sha" ]; then
        applied+=("$target")
        skipped+=("$target")
        continue
      fi
      cp --parents "$target" "$backup_dir"/
    fi
    install -m 0644 "$TRANSLATION_FILE" "$target"
    applied+=("$target")
    updated+=("$target")
  done
  if [ ! -s "$dir/en.json" ]; then
    printf '{}\n' > "$dir/en.json"
    chmod 0644 "$dir/en.json"
  fi
done

patched_nginx=()
for nginx_file in "${nginx_files[@]}"; do
  if [ -f "$nginx_file" ]; then
    patch_nginx_admin_i18n_route "$nginx_file"
    patched_nginx+=("$nginx_file")
  fi
done

version="$(tr -d '[:space:]' < "$APP_DIR/VERSION")"
visual_asset_hash=""
if [ -s "$VISUAL_ASSET_SRC" ]; then
  visual_asset_hash="$(python3 - "$VISUAL_ASSET_SRC" <<'PY'
import hashlib
import sys
from pathlib import Path

print(hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest()[:12])
PY
)"
fi
visual_asset_version="$version"
if [ -n "$visual_asset_hash" ]; then
  visual_asset_version="$version-$visual_asset_hash"
fi
visual_assets=()
patched_html=()
if [ -s "$VISUAL_ASSET_SRC" ]; then
  for admin_root in "${admin_ui_roots[@]}"; do
    if [ -d "$admin_root" ]; then
      install -d -m 0755 "$admin_root/custom-ptbr"
      install -m 0644 "$VISUAL_ASSET_SRC" "$admin_root/$VISUAL_ASSET_REL"
      visual_assets+=("$admin_root/$VISUAL_ASSET_REL")
    fi
  done
  for html_file in "${admin_html_files[@]}"; do
    if [ -f "$html_file" ]; then
      patch_admin_html_visual_i18n "$html_file" "/static/iris/carbonio-admin-ui/$VISUAL_ASSET_REL?v=$visual_asset_version"
      patched_html+=("$html_file")
    fi
  done
fi

applied_json="$(printf '%s\n' "${applied[@]}" | python3 -c 'import json,sys; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))')"
updated_json="$(printf '%s\n' "${updated[@]}" | python3 -c 'import json,sys; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))')"
skipped_json="$(printf '%s\n' "${skipped[@]}" | python3 -c 'import json,sys; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))')"
patched_nginx_json="$(printf '%s\n' "${patched_nginx[@]}" | python3 -c 'import json,sys; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))')"
visual_assets_json="$(printf '%s\n' "${visual_assets[@]}" | python3 -c 'import json,sys; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))')"
patched_html_json="$(printf '%s\n' "${patched_html[@]}" | python3 -c 'import json,sys; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))')"

python3 - "$STATUS_FILE" "$MODULE_ID" "$version" "$sha" "$backup_dir" "$applied_json" "$updated_json" "$skipped_json" "$patched_nginx_json" "$visual_assets_json" "$patched_html_json" <<'PY'
import json
import sys
from datetime import datetime, timezone

status_file, module_id, version, sha, backup_dir, applied_json, updated_json, skipped_json, patched_nginx_json, visual_assets_json, patched_html_json = sys.argv[1:]
data = {
    "module": module_id,
    "version": version,
    "locale": "pt-BR",
    "translation_sha256": sha,
    "last_applied_utc": datetime.now(timezone.utc).isoformat(),
    "backup_dir": backup_dir,
    "applied_files": json.loads(applied_json),
    "updated_files": json.loads(updated_json),
    "skipped_files": json.loads(skipped_json),
    "patched_nginx_files": json.loads(patched_nginx_json),
    "visual_i18n_assets": json.loads(visual_assets_json),
    "patched_html_files": json.loads(patched_html_json),
    "result": "ok",
}
with open(status_file, "w", encoding="utf-8") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
PY

chmod 0644 "$STATUS_FILE"
echo "$MODULE_ID repair ok"
