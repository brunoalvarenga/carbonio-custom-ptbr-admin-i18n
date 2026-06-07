# Homologacao PT-BR Admin I18n

Data: 2026-06-07
Versao: 0.1.0

## Status

HOMOLOGADO PARA USO DO MODULO DE TRADUCAO PT-BR DO ADMIN CONSOLE.

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

## Evidencias

- Prints e resultado web: `build/ptbr-i18n-web-audit-20260607T080912-final/`
- Pacote: `build/xcarbonio/carbonio-custom-ptbr-admin-i18n-0.1.0.zip`

## Pendencias

- Revisao humana fina de todas as `2276` chaves para melhorar frases longas de
  areas pouco usadas. O modulo ja cobre as chaves e as telas principais, mas a
  qualidade linguistica pode ser refinada incrementalmente.
