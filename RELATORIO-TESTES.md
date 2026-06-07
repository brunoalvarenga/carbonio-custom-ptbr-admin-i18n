# Relatorio De Testes

Modulo: Carbonio Custom PT-BR Admin I18n
Versao: 0.1.3
Data: 2026-06-07

## Conclusao

HOMOLOGADO PARA USO DO MODULO DE TRADUCAO PT-BR DO ADMIN CONSOLE.

O modulo foi instalado no servidor `31.220.81.200`, aplicou `pt.json` e aliases
nos caminhos reais do Carbonio Admin, ativou timer/watcher de reaplicacao,
corrigiu a rota Nginx de i18n dos apps nativos e foi validado no navegador com
usuario administrador em `pt_BR`.

Escopo auditado: traducao nativa do Carbonio Admin Console. Itens do roteiro
original ligados a Webmail, tradutor visual, traducao de conteudo de mensagens,
HTML, assinaturas e permissoes de uma tela propria foram classificados como
`NAO APLICAVEL` para este modulo.

## Validacoes Locais

- `python3 scripts/generate-ptbr.py`: extraiu `1834` chaves do Admin Console.
- `translations/pt.json`: gerado com `2276` chaves.
- `bash scripts/smoke-test.sh`: passou.
- `bash -n install.sh repair.sh uninstall.sh scripts/package-release.sh`: passou.
- `python3 -m py_compile scripts/generate-ptbr.py`: passou.
- ZIP final em `build/xcarbonio`: sem `.git`, caches, ZIP antigo ou tarball
  embutido.
- SHA256 do pacote final registrado na release GitHub e no resumo de entrega.

## Validacoes No Servidor

- Versao instalada: `0.1.3`.
- Timer `carbonio-custom-ptbr-admin-i18n-guard.timer`: `enabled/active`.
- Watcher `carbonio-custom-ptbr-admin-i18n.path`: `enabled/active`.
- `nginx -t`: aprovado.
- `/var/lib/carbonio-custom-ptbr-admin-i18n/status.json`: JSON valido.
- `/static/iris/i18n/pt.json`: `200`.
- `/static/iris/carbonio-admin-ui/i18n/pt.json`: `200`.
- `/carbonioAdmin/src/i18n/pt.json`: `200` com `application/json`.
- Simulacao de overwrite para `{}` em `carbonio-admin-ui/i18n/pt.json`: watcher
  restaurou automaticamente para `2276` chaves.

## Bugs Corrigidos

- Empacotamento corrigido para gerar ZIP em `build/xcarbonio`.
- Aliases `pt_BR.json` e `pt-BR.json` adicionados aos mesmos destinos de
  `pt.json`.
- Repair tornado idempotente por hash para permitir watcher sem loop.
- Adicionado `systemd.path` para reaplicar imediatamente quando o bundle recriar
  arquivos `i18n`.
- Adicionada location Nginx para `/carbonioAdmin/src/i18n/`, evitando retorno
  HTML onde o i18next espera JSON.

## Validacoes Web

Usuario de teste: `xcaudit-admin-final@email.smsenviar.com.br`.

Rotas validadas:

- `/carbonioAdmin/`
- `/carbonioAdmin/manage/domains`
- `/carbonioAdmin/manage/domains/global/accounts`
- `/carbonioAdmin/services/custom-activesync`

Resultado Playwright:

- Sem respostas HTTP ruins no escopo auditado.
- Sem erros reais de console; ruido conhecido de SOAP `422` foi registrado como
  nao relacionado ao i18n.
- Textos PT-BR visiveis em Home, Dominios, Accounts e ActiveSync.
- Amostras criticas:
  - `Dashboard` -> `Painel`.
  - `Last access` -> `Último acesso`.
  - `Quick Access to` -> `Acesso rápido a`.
  - `Domain Name` -> `Nome do domínio`.
  - `Create Account Wizard` -> `Assistente de criação de conta`.
  - `Surname` -> `Sobrenome`.
  - `Password` -> `Senha`.
  - `CREATE WITH THESE DATA` -> `CRIAR COM ESTES DADOS`.
  - `Account Status` -> `Status da conta`.

Evidencias:

- `build/ptbr-i18n-web-audit-20260607T1139-final/`

## Observacoes

- O Carbonio Admin escolhe o idioma pela conta (`zimbraPrefLocale` ou
  `zimbraLocale`). A conta de teste foi ajustada para `pt_BR`.
- O modulo nao altera automaticamente todos os usuarios. Para cada admin ver
  PT-BR, a conta ou COS precisa usar locale portugues.
- Termos tecnicos como COS, MTA, LDAP, SOAP, ActiveSync e Z-Push foram
  preservados.
- O modulo nao fornece UI propria nem API propria; por isso nao ha acao
  administrativa nova para usuario comum, delegado ou limitado executar.
- O modulo altera arquivos de traducao e patch controlado de Nginx, sempre com
  backup em `/var/backups/carbonio-custom-ptbr-admin-i18n`.
