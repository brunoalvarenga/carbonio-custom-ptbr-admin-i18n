#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 -m json.tool translations/pt.json >/dev/null
bash -n install.sh repair.sh uninstall.sh scripts/package-release.sh scripts/smoke-test.sh
python3 -m py_compile scripts/generate-ptbr.py scripts/audit-mixed-strings.py
python3 scripts/audit-mixed-strings.py
test -s assets/ptbr-visual-i18n.js
grep -q 'Saturday' assets/ptbr-visual-i18n.js
grep -q 'Sábado' assets/ptbr-visual-i18n.js

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
    "cos.prevent_user_from_changing_password": "Impedir que o usuário altere a senha",
    "quarantine.refresh_list": "ATUALIZAR LISTA",
    "wsc.section.content.description.enableFeature": "Ativar mensagens, chats em grupo, chamadas de vídeo e compartilhamento de arquivos.",
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
