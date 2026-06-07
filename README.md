# Carbonio Custom PT-BR Admin I18n

Modulo para aplicar traducao PT-BR no Carbonio Admin Console e nos modulos
customizados carregados pelo Admin UI.

O modulo usa o mecanismo nativo `i18next` do Carbonio. Ele nao injeta uma
camada visual por cima da interface, nao cria tela propria e nao traduz o
Webmail nem conteudo de mensagens.

A protecao pos-atualizacao usa timer e watcher systemd para reaplicar a
traducao quando o bundle do Admin recriar arquivos `i18n`.

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
- aliases `pt_BR.json` e `pt-BR.json` nos mesmos diretorios, para cobrir
  clientes que usem locale completo em vez de `pt`

Backups ficam em:

```text
/var/backups/carbonio-custom-ptbr-admin-i18n
```

Status da ultima aplicacao:

```text
/var/lib/carbonio-custom-ptbr-admin-i18n/status.json
```

## Pacote

```bash
bash scripts/package-release.sh
```

O ZIP final e gerado em:

```text
build/xcarbonio/carbonio-custom-ptbr-admin-i18n-<versao>.zip
```
