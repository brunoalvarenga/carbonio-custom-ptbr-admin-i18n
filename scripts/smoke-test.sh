#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 -m json.tool translations/pt.json >/dev/null
bash -n install.sh repair.sh uninstall.sh scripts/package-release.sh scripts/smoke-test.sh

python3 - <<'PY'
import json
from pathlib import Path

data = json.loads(Path("translations/pt.json").read_text(encoding="utf-8"))
required = {
    "account.new.create_account_wizard": "Assistente de criação de conta",
    "label.surname": "Sobrenome",
    "label.password": "Senha",
    "commons.create_with_there_data": "CRIAR COM ESTES DADOS",
    "label.account_status": "Status da conta",
}
missing = []
for key, expected in required.items():
    if data.get(key) != expected:
        missing.append(f"{key}={data.get(key)!r}")
if missing:
    raise SystemExit("traducoes criticas ausentes: " + ", ".join(missing))
if len(data) < 1500:
    raise SystemExit(f"pt.json pequeno demais: {len(data)} chaves")
print(f"pt.json ok: {len(data)} chaves")
PY

echo "carbonio-custom-ptbr-admin-i18n smoke ok"
