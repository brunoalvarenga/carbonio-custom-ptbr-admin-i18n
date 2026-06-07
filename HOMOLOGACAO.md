# Homologacao PT-BR Admin I18n

Data: 2026-06-07
Versao: 0.1.4

## Status

HOMOLOGADO PARA USO DO MODULO DE TRADUCAO PT-BR DO ADMIN CONSOLE.

## Escopo Homologado

- Carbonio Admin Console e modulos customizados carregados pelo Admin UI.
- Traducao nativa via arquivos `i18next`.
- Ponte visual controlada para textos dinamicos ja renderizados pelo Admin UI
  fora do `i18next`, como nomes de dias da semana vindos de `date-fns` sem
  locale e enums simples exibidos em tabelas.
- Reaplicacao automatica por timer e watcher systemd apos atualizacoes do
  Carbonio.
- Rota Nginx protegida para servir `/carbonioAdmin/src/i18n/*.json` como JSON,
  evitando fallback para HTML do SPA.
- Sem tela propria, sem API propria e sem dependencia de comando manual para uso
  normal apos instalado.

## Fora Do Escopo

- Webmail, calendario, contatos e cliente final.
- Tradutor visual generico sobreposto a tela. O modulo usa apenas uma ponte
  visual restrita para valores conhecidos que chegam fora do `i18next`.
- Traducao de conteudo de mensagens, HTML, assinaturas ou respostas de e-mail.
- Testes de permissao de usuario comum em uma UI propria, pois o modulo nao
  expoe operacoes administrativas pela interface.

## Acesso

O modulo nao cria uma tela propria. Ele aplica traducao nativa via i18next no
Carbonio Admin Console.

Para visualizar em PT-BR, a conta administrativa deve estar com locale:

```text
zimbraPrefLocale: pt_BR
zimbraLocale: pt_BR
```

## Resultado

- Servidor validado: `31.220.81.200`.
- Arquivos de traducao aplicados em `/opt/zextras/admin/iris`.
- Asset visual aplicado em `/static/iris/carbonio-admin-ui/custom-ptbr/`.
- Timer de reaplicacao e watcher `.path` ativos.
- Endpoints de traducao retornando `200` com JSON real.
- Admin Console renderizando textos em PT-BR.
- Evidencias web geradas por Playwright.
- Auditoria do roteiro de traducao Admin/Webmail classificada como parcialmente
  nao aplicavel ao modulo atual, por diferenca de escopo.

## Bugs Encontrados E Corrigidos

- O script de pacote gerava ZIP na raiz do modulo, enquanto a entrega esperada
  era `build/xcarbonio`.
- `/static/iris/carbonio-admin-ui/i18n/pt.json` podia ser recriado como `{}` pelo
  bundle do Admin; corrigido com repair idempotente, aliases e watcher systemd.
- `/carbonioAdmin/src/i18n/pt.json` retornava HTML do fallback React; corrigido
  com location Nginx especifica para `i18n`.
- `Último acesso` exibia o dia da semana em ingles, por exemplo `Saturday`,
  porque o timestamp era formatado por `date-fns` sem locale antes de chegar ao
  componente. Corrigido com asset visual idempotente do modulo, validado como
  `Último acesso Sábado 06 Jun 2026 | 8:22 PM`.
- Preferencias de COS ainda tinham frases hibridas como `Add invites com PUBLISH
  method`, `Use iCal delegation model para shared calendars`, `Receiving Mails`
  e `Contato Options`; corrigidas com chaves curadas no `pt.json`.
- Pente fino adicional em Dominios/Global/Configuracoes corrigiu
  `Allow searching users' information in all domains`, `Domain System
  Notifications` e textos de aviso legal/disclaimer.
- Pente fino adicional em Contas corrigiu lista, perfil, campos de telefone,
  empresa, endereco, sessoes ativas, busca, data de criacao, observacoes,
  quota e valores dinamicos como `DelegatedAdmin`, `System`, `Locked` e
  `Unlimited`.
- Pente fino final corrigiu sobras hibridas do dicionario como `Forgotten
  Senha`, `Passwords do not match`, `Senha should be more than 5 character`,
  `One Hora Senha management`, `Tuning Options`, `Geral Options`, `Can access
  Configurações` e `E-mail Options`.
- A chave ambigua `label.home`, usada pelo upstream tanto no breadcrumb quanto
  no telefone residencial, foi tratada com `Residencial` no dicionario e
  correcao visual restrita para manter o breadcrumb como `Início`.

## Evidencias

- Prints e resultado web: `build/ptbr-i18n-web-audit-20260607T1314-0.1.4-pente-fino/`
- Pacote: `build/xcarbonio/carbonio-custom-ptbr-admin-i18n-0.1.4.zip`
- SHA256 do pacote final: registrado no resumo de entrega e na release GitHub.
- Revalidacao pos-cachebuster no Chrome ficou limitada pela tela de login com
  sessao expirada; a instalacao final foi validada por arquivo aplicado, hash,
  cachebuster `0.1.4-fcfbe1c16a20`, HTTP `200`, `nginx -t` e auditoria local.

## Pendencias

- Revisao humana fina de todas as `2279` chaves para melhorar frases longas de
  areas pouco usadas. A auditoria atual corrigiu as telas reportadas e os
  residuos mais visiveis em COS, Quarentena, Chat/WSC, Backup, MTA e datas.
