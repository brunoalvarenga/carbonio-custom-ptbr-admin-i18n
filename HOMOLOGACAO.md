# Homologacao PT-BR Admin I18n

Data: 2026-06-07
Versao: 0.1.3

## Status

HOMOLOGADO PARA USO DO MODULO DE TRADUCAO PT-BR DO ADMIN CONSOLE.

## Escopo Homologado

- Carbonio Admin Console e modulos customizados carregados pelo Admin UI.
- Traducao nativa via arquivos `i18next`.
- Reaplicacao automatica por timer e watcher systemd apos atualizacoes do
  Carbonio.
- Rota Nginx protegida para servir `/carbonioAdmin/src/i18n/*.json` como JSON,
  evitando fallback para HTML do SPA.
- Sem tela propria, sem API propria e sem dependencia de comando manual para uso
  normal apos instalado.

## Fora Do Escopo

- Webmail, calendario, contatos e cliente final.
- Tradutor visual sobreposto a tela.
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

## Evidencias

- Prints e resultado web: `build/ptbr-i18n-web-audit-20260607T1139-final/`
- Pacote: `build/xcarbonio/carbonio-custom-ptbr-admin-i18n-0.1.3.zip`
- SHA256 do pacote final: registrado na release GitHub e no resumo de entrega.

## Pendencias

- Revisao humana fina de todas as `2276` chaves para melhorar frases longas de
  areas pouco usadas. O modulo ja cobre as chaves e as telas principais, mas a
  qualidade linguistica pode ser refinada incrementalmente.
