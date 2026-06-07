# Carbonio Custom PT-BR Admin I18n

Modulo para aplicar traducao PT-BR no Carbonio Admin Console e nos modulos
customizados carregados pelo Admin UI.

O modulo usa o mecanismo nativo `i18next` do Carbonio. Ele nao injeta uma
camada visual por cima da interface.

## Instalar

```bash
bash install.sh
```

## Reparar/Reaplicar

```bash
bash repair.sh
```

## Remover

```bash
bash uninstall.sh
```

O uninstall restaura o backup mais recente quando houver backup disponivel.

## Arquivos Aplicados

- `/opt/zextras/admin/iris/i18n/pt.json`
- `/opt/zextras/admin/iris/carbonio-admin-ui/i18n/pt.json`
- `/opt/zextras/admin/iris/src/i18n/pt.json`
- caminhos equivalentes sob `carbonio-admin-ui/current` e `carbonio-admin-ui/src`

Backups ficam em:

```text
/var/backups/carbonio-custom-ptbr-admin-i18n
```

Status da ultima aplicacao:

```text
/var/lib/carbonio-custom-ptbr-admin-i18n/status.json
```
