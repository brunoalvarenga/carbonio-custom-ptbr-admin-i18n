# Relatorio De Testes

Modulo: Carbonio Custom PT-BR Admin I18n
Versao: 0.1.4
Data: 2026-06-07

## Conclusao

HOMOLOGADO PARA USO DO MODULO DE TRADUCAO PT-BR DO ADMIN CONSOLE.

O modulo foi instalado no servidor `31.220.81.200`, aplicou `pt.json` e aliases
nos caminhos reais do Carbonio Admin, ativou timer/watcher de reaplicacao,
corrigiu a rota Nginx de i18n dos apps nativos, adicionou uma ponte visual
restrita para textos dinamicos fora do `i18next` e foi validado no navegador
com usuario administrador em `pt_BR`.

Escopo auditado: traducao nativa do Carbonio Admin Console, com ponte visual
limitada a nomes de dias/meses ja formatados em ingles. Itens do roteiro
original ligados a Webmail, tradutor visual generico, traducao de conteudo de
mensagens, HTML, assinaturas e permissoes de uma tela propria foram
classificados como `NAO APLICAVEL` para este modulo.

## Validacoes Locais

- `python3 scripts/generate-ptbr.py`: extraiu `1834` chaves do Admin Console.
- `translations/pt.json`: gerado com `2279` chaves.
- `bash scripts/smoke-test.sh`: passou.
- `bash -n install.sh repair.sh uninstall.sh scripts/package-release.sh`: passou.
- `python3 -m py_compile scripts/generate-ptbr.py`: passou.
- `python3 scripts/audit-mixed-strings.py`: passou com 74 chaves criticas
  verificadas.
- `assets/ptbr-visual-i18n.js`: validado com mapa `Saturday` -> `Sábado`.
- ZIP final em `build/xcarbonio`: sem `.git`, caches, ZIP antigo ou tarball
  embutido.
- SHA256 do pacote final registrado no resumo de entrega e na release GitHub.

## Validacoes No Servidor

- Versao instalada: `0.1.4`.
- Timer `carbonio-custom-ptbr-admin-i18n-guard.timer`: `enabled/active`.
- Watcher `carbonio-custom-ptbr-admin-i18n.path`: `enabled/active`.
- `nginx -t`: aprovado.
- `/var/lib/carbonio-custom-ptbr-admin-i18n/status.json`: JSON valido.
- `/static/iris/i18n/pt.json`: `200`.
- `/static/iris/carbonio-admin-ui/i18n/pt.json`: `200`.
- `/carbonioAdmin/src/i18n/pt.json`: `200` com `application/json`.
- `/static/iris/carbonio-admin-ui/custom-ptbr/ptbr-visual-i18n.js`: `200`.
- Cachebuster aplicado no `index.html`:
  `ptbr-visual-i18n.js?v=0.1.4-fcfbe1c16a20`.
- Simulacao de overwrite para `{}` em `carbonio-admin-ui/i18n/pt.json`: watcher
  restaurou automaticamente para `2279` chaves.

## Bugs Corrigidos

- Empacotamento corrigido para gerar ZIP em `build/xcarbonio`.
- Aliases `pt_BR.json` e `pt-BR.json` adicionados aos mesmos destinos de
  `pt.json`.
- Repair tornado idempotente por hash para permitir watcher sem loop.
- Adicionado `systemd.path` para reaplicar imediatamente quando o bundle recriar
  arquivos `i18n`.
- Adicionada location Nginx para `/carbonioAdmin/src/i18n/`, evitando retorno
  HTML onde o i18next espera JSON.
- Adicionado asset visual idempotente para traduzir nomes de dias/meses e
  alguns enums/textos dinamicos ja renderizados em ingles, corrigindo
  `Último acesso Saturday...`, `DelegatedAdmin`, `System`, `Locked` e
  `Unlimited`.
- Corrigidas frases hibridas reportadas em Preferencias de COS, incluindo
  `Add invites com PUBLISH method`, `Use iCal delegation model para shared
  calendars`, `Receiving Mails`, `Sending Mails`, `Contato Options`, `Use GAL
  para auto-fill` e `Work Week Visualizar`.
- Corrigidos residuos reportados em Dominios/Global/Configuracoes:
  `Domain System Notifications`, `Only allow outbound disclaimers` e `Allow
  searching users' information in all domains`.
- Corrigidos residuos em Contas/Perfil: abas `GENERAL/PROFILE`, campos
  `Phone`, `Mobile`, `Company`, `Job Title`, `Country`, `State`, `City`,
  `Postal Code`, lista de contas, busca, data de criacao, observacoes, sessoes
  ativas e quota.
- Corrigidas sobras hibridas do dicionario encontradas no pente fino final:
  `Forgotten Senha`, `Passwords do not match`, `Senha should be more than 5
  character`, `One Hora Senha management`, `Tuning Options`, `Geral Options`,
  `Can access Configurações` e `E-mail Options`.
- A chave `label.home` e ambigua no upstream. O modulo agora usa `Residencial`
  para o campo de telefone e a ponte visual restrita preserva `Início` no
  breadcrumb.

## Validacoes Web

Usuario de teste: `xcaudit-admin-final@email.smsenviar.com.br`.

Rotas validadas:

- `/carbonioAdmin/`
- `/carbonioAdmin/manage/domains`
- `/carbonioAdmin/manage/domains/global/accounts`
- `/carbonioAdmin/manage/domains/global/settings`
- `/carbonioAdmin/manage/domains/9e6f0156-0e4d-44f4-8aee-76d8b727f08d/accounts`
- `/carbonioAdmin/manage/cos`
- `/carbonioAdmin/manage/cos/e00428a1-0c00-11d9-836a-000d93afea2a/preferences`
- `/carbonioAdmin/manage/cos/e00428a1-0c00-11d9-836a-000d93afea2a/features`
- `/carbonioAdmin/services/custom-activesync`

Resultado Playwright:

- Sem respostas HTTP ruins no escopo auditado.
- Sem erros reais de console; ruido conhecido de SOAP `422` foi registrado como
  nao relacionado ao i18n.
- Textos PT-BR visiveis em Home, Dominios, Accounts e ActiveSync.
- Texto de data validado no Chrome:
  - `Último acesso Saturday 06 Jun 2026 | 8:22 PM` -> `Último acesso Sábado 06
    Jun 2026 | 8:22 PM`.
- Preferencias de COS sem as frases proibidas da auditoria.
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
  - `Allow searching users' information in all domains` -> `Permitir pesquisa de
    informações de usuários em todos os domínios`.
  - `Phone` -> `Telefone`.
  - `Job Title` -> `Cargo`.
  - `Postal Code` -> `CEP`.

Evidencias:

- `build/ptbr-i18n-web-audit-20260607T1314-0.1.4-pente-fino/`
- Revalidacao visual pos-cachebuster no Chrome: sessao expirada na tela de
  login, sem reenvio de credencial pelo navegador. Validacao final confirmada
  por instalacao no servidor, `pt.json` com `2279` chaves, cachebuster,
  endpoints HTTP `200`, `nginx -t`, `systemctl --failed` sem unidades e smoke
  local.

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
