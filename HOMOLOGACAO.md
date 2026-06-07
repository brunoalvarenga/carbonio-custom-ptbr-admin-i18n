# Homologacao PT-BR Admin I18n

Data: 2026-06-07
Versao: 0.1.2

## Status

HOMOLOGADO PARA USO DO MODULO DE TRADUCAO PT-BR DO ADMIN CONSOLE.

## Escopo Homologado

- Carbonio Admin Console e modulos customizados carregados pelo Admin UI.
- Traducao nativa via arquivos `i18next`.
- Reaplicacao automatica por timer systemd apos atualizacoes do Carbonio.
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
- Timer de reaplicacao ativo.
- Endpoints de traducao retornando `200`.
- Admin Console renderizando textos em PT-BR.
- Evidencias web geradas por Playwright.
- Auditoria do roteiro de traducao Admin/Webmail classificada como parcialmente
  nao aplicavel ao modulo atual, por diferenca de escopo.

## Evidencias

- Prints e resultado web: `build/ptbr-i18n-web-audit-20260607T080912-final/`
- Pacote: `build/xcarbonio/carbonio-custom-ptbr-admin-i18n-0.1.2.zip`

## Pendencias

- Revisao humana fina de todas as `2276` chaves para melhorar frases longas de
  areas pouco usadas. O modulo ja cobre as chaves e as telas principais, mas a
  qualidade linguistica pode ser refinada incrementalmente.
