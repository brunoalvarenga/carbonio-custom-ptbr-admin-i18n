# Relatorio De Testes

Modulo: Carbonio Custom PT-BR Admin I18n
Versao: 0.1.2
Data: 2026-06-07

## Conclusao

HOMOLOGADO PARA USO DO MODULO DE TRADUCAO PT-BR DO ADMIN CONSOLE.

O modulo foi instalado no servidor `31.220.81.200`, aplicou `pt.json` nos
caminhos reais do Carbonio Admin, ativou timer de reaplicacao e foi validado no
navegador com usuario administrador em `pt_BR`.

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

## Validacoes No Servidor

- Versao instalada: `0.1.2`.
- Timer `carbonio-custom-ptbr-admin-i18n-guard.timer`: `enabled/active`.
- `nginx -t`: aprovado.
- `/var/lib/carbonio-custom-ptbr-admin-i18n/status.json`: JSON valido.
- `/static/iris/i18n/pt.json`: `200`.
- `/static/iris/carbonio-admin-ui/i18n/pt.json`: `200`.

## Validacoes Web

Usuario de teste: `xcaudit-admin-final@email.smsenviar.com.br`.

Rotas validadas:

- `/carbonioAdmin/`
- `/carbonioAdmin/manage/domains`
- `/carbonioAdmin/services/custom-activesync`

Resultado Playwright:

- Sem respostas HTTP ruins no escopo `carbonioAdmin/static/iris`.
- Sem erros de console.
- Textos PT-BR visiveis em Home, Dominios e ActiveSync.
- Amostras criticas:
  - `Create Account Wizard` -> `Assistente de criação de conta`.
  - `Surname` -> `Sobrenome`.
  - `Password` -> `Senha`.
  - `CREATE WITH THESE DATA` -> `CRIAR COM ESTES DADOS`.
  - `Account Status` -> `Status da conta`.

Evidencias:

- `build/ptbr-i18n-web-audit-20260607T080912-final/`

## Observacoes

- O Carbonio Admin escolhe o idioma pela conta (`zimbraPrefLocale` ou
  `zimbraLocale`). A conta de teste foi ajustada para `pt_BR`.
- O modulo nao altera automaticamente todos os usuarios. Para cada admin ver
  PT-BR, a conta ou COS precisa usar locale portugues.
- Termos tecnicos como COS, MTA, LDAP, SOAP, ActiveSync e Z-Push foram
  preservados.
- O modulo nao fornece UI propria nem API propria; por isso nao ha acao
  administrativa nova para usuario comum, delegado ou limitado executar.
