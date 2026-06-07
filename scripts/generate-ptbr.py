#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path


EXACT_TRANSLATIONS: dict[str, str] = {
    "Account": "Conta",
    "Accounts": "Contas",
    "Account Name": "Nome da conta",
    "Account Status": "Status da conta",
    "Active": "Ativo",
    "ActiveSync": "ActiveSync",
    "Add": "Adicionar",
    "Add Account": "Adicionar conta",
    "Add Domain": "Adicionar domínio",
    "Address": "Endereço",
    "Admin": "Administrador",
    "Admin Console": "Console de administração",
    "Advanced": "Avançado",
    "Aliases": "Aliases",
    "All": "Todos",
    "Allow": "Permitir",
    "Apply": "Aplicar",
    "Are you sure?": "Tem certeza?",
    "Authentication": "Autenticação",
    "Authorized Senders": "Remetentes autorizados",
    "Backup": "Backup",
    "Backups": "Backups",
    "Bucket": "Bucket",
    "Buckets": "Buckets",
    "Cancel": "Cancelar",
    "Certificate": "Certificado",
    "Certificates": "Certificados",
    "Change Password": "Alterar senha",
    "Close": "Fechar",
    "Confirm": "Confirmar",
    "Contacts": "Contatos",
    "COS": "COS",
    "Create": "Criar",
    "Create Account Wizard": "Assistente de criação de conta",
    "Create New COS": "Criar novo COS",
    "CREATE WITH THESE DATA": "CRIAR COM ESTES DADOS",
    "Created": "Criado",
    "Dashboard": "Painel",
    "Default": "Padrão",
    "Default COS": "COS padrão",
    "Delete": "Excluir",
    "Delegated Admin": "Administrador delegado",
    "Description": "Descrição",
    "Details": "Detalhes",
    "Disable": "Desativar",
    "Disabled": "Desativado",
    "Display Name": "Nome de exibição",
    "Display Name (Auto-fill)": "Nome de exibição (preenchimento automático)",
    "Domain": "Domínio",
    "Domain Admin": "Administrador do domínio",
    "Domain Name": "Nome do domínio",
    "Domains": "Domínios",
    "Done": "Concluído",
    "Edit": "Editar",
    "Email": "E-mail",
    "Enable": "Ativar",
    "Enabled": "Ativado",
    "Error": "Erro",
    "Errors": "Erros",
    "Filter": "Filtro",
    "General": "Geral",
    "General Settings": "Configurações gerais",
    "Group": "Grupo",
    "Groups": "Grupos",
    "Help Desk Admin": "Administrador de suporte",
    "Hide": "Ocultar",
    "Host": "Host",
    "Hostname": "Nome do host",
    "Language": "Idioma",
    "List": "Lista",
    "Loading": "Carregando",
    "Login": "Login",
    "Logout": "Sair",
    "Mail": "E-mail",
    "Mailbox": "Caixa postal",
    "Mailing List": "Lista de distribuição",
    "Mailing Lists": "Listas de distribuição",
    "Manage": "Gerenciar",
    "Management": "Gerenciamento",
    "Middle Name Initials": "Iniciais do nome do meio",
    "MTA": "MTA",
    "Name": "Nome",
    "New": "Novo",
    "Next": "Próximo",
    "No": "Não",
    "Notifications": "Notificações",
    "OK": "OK",
    "Operations": "Operações",
    "Password": "Senha",
    "Password*": "Senha*",
    "Pending": "Pendente",
    "Permission": "Permissão",
    "Permissions": "Permissões",
    "Preferences": "Preferências",
    "Privacy": "Privacidade",
    "Queued": "Na fila",
    "Quota": "Cota",
    "Remove": "Remover",
    "Repeat Password": "Repetir senha",
    "Repeat Password*": "Repetir senha*",
    "Reset": "Redefinir",
    "Resources": "Recursos",
    "Restore": "Restaurar",
    "Retry": "Tentar novamente",
    "Running": "Em execução",
    "Save": "Salvar",
    "Search": "Pesquisar",
    "Server": "Servidor",
    "Servers": "Servidores",
    "Service": "Serviço",
    "Services": "Serviços",
    "Settings": "Configurações",
    "Show": "Exibir",
    "Status": "Status",
    "Storage": "Armazenamento",
    "Surname": "Sobrenome",
    "Time Zone": "Fuso horário",
    "Type": "Tipo",
    "Update": "Atualizar",
    "User": "Usuário",
    "User Management Admin": "Administrador de usuários",
    "User will change password on next login": "O usuário alterará a senha no próximo login",
    "Users": "Usuários",
    "View": "Visualizar",
    "Volume": "Volume",
    "Volumes": "Volumes",
    "Warning": "Aviso",
    "Yes": "Sim",
    "Changes have been saved successfully": "Alterações salvas com sucesso",
    "Something went wrong": "Algo deu errado",
    "There are no items to show": "Não há itens para exibir",
    "No results found": "Nenhum resultado encontrado",
    "Search results": "Resultados da pesquisa",
}


KEY_TRANSLATIONS: dict[str, str] = {
    "accountDetails.auto_fill_user_is_disabled": "Preenchimento automático do usuário desativado",
    "accountDetails.default_COS": "COS padrão",
    "accountDetails.user_will_change_password_on_next_login": "O usuário alterará a senha no próximo login",
    "account.new.create_account_wizard": "Assistente de criação de conta",
    "account.new.create_otp_wizard": "Assistente de criação de OTP",
    "account_details.ADD": "ADICIONAR",
    "account_details.DELETE": "EXCLUIR",
    "account_details.NEXT": "PRÓXIMO",
    "account_details.a_user": "Um usuário",
    "account_details.able_to_see_password_once": "Atenção: você poderá ver a senha <bold>apenas uma vez.</bold>",
    "account_details.abq_status": "Status ABQ",
    "account_details.account_with_read_only_rights": "Contas com permissão <bold>somente leitura</bold>",
    "account_details.account_with_read_write_rights": "Contas com permissão <bold>leitura/gravação</bold>",
    "account_details.account_with_send_rights": "Conta com permissões <bold>Enviar como/Enviar em nome de</bold>",
    "account_details.add_forwarded_invites_to_calendar": "Adicionar automaticamente compromissos encaminhados ao calendário",
    "account_details.add_the_account_group_with_selected_rights": "ADICIONAR A CONTA/GRUPO COM AS PERMISSÕES SELECIONADAS",
    "account_details.add_user_on_delegates_list": "Adicionar usuário à lista de delegados",
    "account_details.allow_sending_cancellation_mail": "Permitir envio de e-mail de cancelamento",
    "account_details.an_existing_group": "Um grupo existente",
    "account_details.appointments_default_duration": "Duração padrão dos compromissos",
    "account_details.as": "como",
    "account_details.as_new_email_arrives": "Quando um novo e-mail chegar",
    "account_details.auto_delete_duplicate_messages": "Excluir automaticamente mensagens duplicadas",
    "account_details.click_on_the_pencil_to_edit": "Clique no lápis para editar o alias disponível ou no X para excluí-lo",
    "account_details.click_to_revert": "Clique para reverter.",
    "account_details.create": "CRIAR",
    "account_details.default_COS": "COS padrão",
    "account_details.default_view.day": "Visualização diária",
    "account_details.default_view.list": "Visualização em lista",
    "account_details.default_view.month": "Visualização mensal",
    "account_details.default_view.week": "Visualização semanal",
    "account_details.default_view.work_week": "Visualização de semana útil",
    "account_details.delegate_created_successfully": "Permissões de delegado criadas com sucesso",
    "account_details.delegate_deleted_successfully": "Permissões de delegado excluídas com sucesso",
    "account_details.delegate_rights": "Permissões do delegado",
    "account_details.delegate_updated_successfully": "Permissões de delegado atualizadas com sucesso",
    "account_details.delegated_administration": "Administração delegada",
    "account_details.delete_password": "Excluir senha",
    "account_details.delete_password_of_user_ldap": "Você está excluindo a senha de <bold>{{name}}</bold> do LDAP. Tem certeza de que deseja excluí-la?",
    "account_details.delete_user_password": "EXCLUIR SENHA DO USUÁRIO NO LDAP",
    "account_details.deligate_abstract_text": "O usuário {{granteeEmail}} poderá enviar e-mails {{right}} {{targetEmail}}",
    "account_details.enable_past_due_reminders": "Ativar lembretes de compromissos no passado",
    "account_details.forwarding_addresses_hidden_from_the_user": "Endereços de encaminhamento ocultos do usuário",
    "account_details.forwarding_addresses_specified_by_the_user": "Endereços de encaminhamento especificados pelo usuário",
    "account_details.forwarding_calendar_invitations_to_these_addresses": "Encaminhar convites de calendário para estes endereços",
    "account_details.global_administration": "Administração global",
    "account_details.hidden_in_gal": "Oculto na GAL",
    "account_details.i_have_copied_the_password": "COPIEI A SENHA",
    "account_details.included_in_backup": "Incluído no backup",
    "account_details.inherited_value_was": "O valor herdado era: {{value}}",
    "account_details.label": "Rótulo",
    "account_details.mail_signature": "Assinatura de e-mail",
    "account_details.manage_aliases": "GERENCIAR ALIASES",
    "account_details.manage_no_rights_to_send_mails": "Gerenciar (sem permissão para enviar e-mails)",
    "account_details.manage_the_aliases_for_this_account": "Gerenciar aliases desta conta",
    "account_details.manuallly": "Manualmente",
    "account_details.new_alias_name": "Novo nome de alias",
    "account_details.on_behalf_of": "em nome de",
    "account_details.otp_devices": "Dispositivos OTP",
    "account_details.passphrasaId": "ID da frase secreta",
    "account_details.read_mails_only": "Ler e-mails apenas (sem permissão para enviar e-mails)",
    "account_details.read_only": "Somente leitura",
    "account_details.read_write": "Leitura/gravação",
    "account_details.remove": "REMOVER",
    "account_details.remove_all": "REMOVER TODOS",
    "account_details.right_for_selected_user_deleted_successfully": "Permissão do usuário selecionado excluída com sucesso",
    "account_details.save_to_sent": "Salvar em enviados",
    "account_details.search_here_for_an_account": "Pesquise uma conta aqui",
    "account_details.secret_code": "Código secreto",
    "account_details.select_mode": "SELECIONAR MODO",
    "account_details.send": "ENVIAR",
    "account_details.send_check": "Enviar",
    "account_details.send_mails_only": "Enviar e-mails apenas (sem permissão para ler pastas)",
    "account_details.send_on_behalf_of_check": "Enviar em nome de",
    "account_details.send_read_manage_mails": "Enviar, ler e gerenciar e-mails (todas as opções acima)",
    "account_details.send_read_mails": "Enviar e ler e-mails (sem permissão para criar pastas ou gerenciar e-mails)",
    "account_details.send_recipients_see_the_mail": "Enviar {{right}} (os destinatários verão este remetente {{targetEmail}})",
    "account_details.send_the_otp_to": "Enviar OTP para",
    "account_details.sendin_options": "Opções de envio",
    "account_details.service_label_password": "Senha de {{ service_label }}",
    "account_details.service_password": "Senha de serviço",
    "account_details.services": "Serviços",
    "account_details.services_passphrase": "Frase secreta de serviços",
    "account_details.services_passphrase_created_successfully": "Frase secreta de serviços criada com sucesso",
    "account_details.services_passphrase_deleted_successfully": "Frase secreta de serviços excluída com sucesso",
    "account_details.set_rights": "DEFINIR PERMISSÕES",
    "account_details.start_typing_account": "Comece a digitar uma conta/grupo para adicionar permissões",
    "account_details.switch_advanced": "Alternar para visualização avançada",
    "account_details.switch_simplified": "Alternar para visualização simplificada",
    "account_details.this_account_is_a_direct_member_of": "Esta conta é membro direto de",
    "account_details.this_account_is_a_in_direct_member_of": "Esta conta é membro indireto de",
    "account_details.this_user_must_change_password": "Este usuário deve alterar a senha",
    "account_details.type_the_new_alias_name": "Digite o novo alias e selecione um domínio para adicioná-lo aos aliases disponíveis",
    "account_details.unlimited": "Ilimitado",
    "account_details.use_gal_to_auto_fill": "Usar GAL para preenchimento automático",
    "account_details.use_ical_delegation_model_for_shared_calendars": "Usar modelo de delegação iCal para calendários compartilhados",
    "account_details.user_can_specify_forwarding_address": "Usuário pode especificar endereço de encaminhamento",
    "account_details.user_can_specify_mail_forwarding_filter": "Usuário pode especificar filtro de encaminhamento de e-mail",
    "account_details.user_password_deleted": "Senha do usuário excluída com sucesso",
    "account_details.user_password_set": "Senha do usuário definida com sucesso",
    "account_details.view_mail_as_html": "Visualizar e-mail como HTML",
    "account_details.what_rights_will_the_delegate_have": "Quais permissões o delegado terá?",
    "account_details.who_will_be_delegates": "Quem serão os delegados?",
    "account_details.your_available_aliases": "Seus aliases disponíveis",
    "commons.create_with_there_data": "CRIAR COM ESTES DADOS",
    "dashboard.core_version": "Versão Core",
    "dashboard.go_to_mailstores_server_list": "Ir para lista de servidores mailstore",
    "dashboard.quick_access_to": "Acesso rápido a",
    "dashboard.server_name": "Nome do servidor",
    "domain.type_the exact_domain_name": "Digite o nome exato do domínio",
    "domain.mailbox_quota": "Cota de caixa postal",
    "label.class_of_service": "Classe de serviço",
    "label.class_of_service_cos": "Classe de serviço (COS)",
    "label.default_class_of_service": "Classe de serviço padrão",
    "label.distribution_list": "Lista de distribuição",
    "label.distribution_lists": "Listas de distribuição",
    "label.domain_primarybar_tooltip": "Visualize os <bold>detalhes dos domínios</bold> e <bold>gerencie</bold> recursos como <bold>contas, listas de distribuição, recursos</bold> e <bold>mais</bold>.",
    "label.global_address_list": "Lista global de endereços",
    "label.items_per_page": "itens por página",
    "label.last_access": "Último acesso",
    "label.mailbox_quota": "Cota de caixa postal",
    "label.mailstores_list": "Lista de mailstores",
    "label.new_distribution_list": "Nova lista de distribuição",
    "label.of": "de",
    "label.quarantine": "Quarentena",
    "label.server_name": "Nome do servidor",
    "label.showing": "Exibindo",
    "label.virtual_hosts": "Hosts virtuais",
    "label.virtual_hosts_and_certificates": "Hosts virtuais e certificado",
    "mta.server_name": "Nome do servidor",
    "quarantine.quarantine": "Quarentena",
    "welcome": "Bem-vindo",
    "label.account_status": "Status da conta",
    "label.advance_edit_display_name": "Nome de exibição",
    "label.default_cos": "COS padrão",
    "label.description": "Descrição",
    "label.display_name": "Nome de exibição",
    "label.display_name_auto_fill": "Nome de exibição (preenchimento automático)",
    "label.domain_name": "Nome do domínio",
    "label.name": "Nome",
    "label.password": "Senha",
    "label.repeat_password": "Repetir senha",
    "label.second_name_initials": "Iniciais do nome do meio",
    "label.surname": "Sobrenome",
    "label.surname_required": "Sobrenome é obrigatório",
    "label.language": "Idioma",
    "label.general_settings": "Configurações gerais",
    "label.management": "Gerenciamento",
    "label.services": "Serviços",
    "label.backup": "Backup",
    "label.active": "Ativo",
    "label.enabled": "Ativado",
    "label.disabled": "Desativado",
    "label.running": "Em execução",
    "label.queued": "Na fila",
    "label.done": "Concluído",
}


WORD_TRANSLATIONS: list[tuple[str, str]] = [
    ("ActiveSync", "ActiveSync"),
    ("Z-Push", "Z-Push"),
    ("LDAP", "LDAP"),
    ("SOAP", "SOAP"),
    ("MTA", "MTA"),
    ("COS", "COS"),
    ("SSL", "SSL"),
    ("TLS", "TLS"),
    ("URL", "URL"),
    ("UUID", "UUID"),
    ("ID", "ID"),
    ("Account", "Conta"),
    ("Accounts", "Contas"),
    ("Alias", "Alias"),
    ("Aliases", "Aliases"),
    ("Admin", "Administrador"),
    ("Administrator", "Administrador"),
    ("Advanced", "Avançado"),
    ("Allowed", "Permitido"),
    ("Allow", "Permitir"),
    ("Apply", "Aplicar"),
    ("Attachment", "Anexo"),
    ("Attachments", "Anexos"),
    ("Auth", "Autenticação"),
    ("Backup", "Backup"),
    ("Backups", "Backups"),
    ("Bucket", "Bucket"),
    ("Calendar", "Calendário"),
    ("Cancel", "Cancelar"),
    ("Certificate", "Certificado"),
    ("Certificates", "Certificados"),
    ("Class of Service", "Classe de serviço"),
    ("Close", "Fechar"),
    ("Confirm", "Confirmar"),
    ("Contact", "Contato"),
    ("Contacts", "Contatos"),
    ("Create", "Criar"),
    ("Created", "Criado"),
    ("Delete", "Excluir"),
    ("Description", "Descrição"),
    ("Detail", "Detalhe"),
    ("Details", "Detalhes"),
    ("Disable", "Desativar"),
    ("Disabled", "Desativado"),
    ("Display", "Exibição"),
    ("Domain", "Domínio"),
    ("Domains", "Domínios"),
    ("Edit", "Editar"),
    ("Email", "E-mail"),
    ("Enable", "Ativar"),
    ("Enabled", "Ativado"),
    ("Error", "Erro"),
    ("Errors", "Erros"),
    ("Export", "Exportar"),
    ("File", "Arquivo"),
    ("Files", "Arquivos"),
    ("Filter", "Filtro"),
    ("General", "Geral"),
    ("Group", "Grupo"),
    ("Groups", "Grupos"),
    ("History", "Histórico"),
    ("Host", "Host"),
    ("Hostname", "Nome do host"),
    ("Import", "Importar"),
    ("Language", "Idioma"),
    ("Last", "Último"),
    ("List", "Lista"),
    ("Loading", "Carregando"),
    ("Login", "Login"),
    ("Logout", "Sair"),
    ("Mail", "E-mail"),
    ("Mailbox", "Caixa postal"),
    ("Manage", "Gerenciar"),
    ("Management", "Gerenciamento"),
    ("Message", "Mensagem"),
    ("Messages", "Mensagens"),
    ("Name", "Nome"),
    ("New", "Novo"),
    ("Next", "Próximo"),
    ("Notification", "Notificação"),
    ("Notifications", "Notificações"),
    ("Operation", "Operação"),
    ("Operations", "Operações"),
    ("Password", "Senha"),
    ("Permission", "Permissão"),
    ("Permissions", "Permissões"),
    ("Policy", "Política"),
    ("Preferences", "Preferências"),
    ("Privacy", "Privacidade"),
    ("Quota", "Cota"),
    ("Remove", "Remover"),
    ("Reset", "Redefinir"),
    ("Resource", "Recurso"),
    ("Resources", "Recursos"),
    ("Restore", "Restaurar"),
    ("Retry", "Tentar novamente"),
    ("Running", "Em execução"),
    ("Save", "Salvar"),
    ("Search", "Pesquisar"),
    ("Server", "Servidor"),
    ("Servers", "Servidores"),
    ("Service", "Serviço"),
    ("Services", "Serviços"),
    ("Setting", "Configuração"),
    ("Settings", "Configurações"),
    ("Status", "Status"),
    ("Storage", "Armazenamento"),
    ("Successful", "Bem-sucedido"),
    ("Successfully", "com sucesso"),
    ("Time", "Hora"),
    ("Timezone", "Fuso horário"),
    ("Type", "Tipo"),
    ("Update", "Atualizar"),
    ("Upload", "Enviar"),
    ("User", "Usuário"),
    ("Users", "Usuários"),
    ("View", "Visualizar"),
    ("Volume", "Volume"),
    ("Volumes", "Volumes"),
    ("Warning", "Aviso"),
]


REGEX_REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^Create (.+)$", re.I), r"Criar \1"),
    (re.compile(r"^Edit (.+)$", re.I), r"Editar \1"),
    (re.compile(r"^Delete (.+)$", re.I), r"Excluir \1"),
    (re.compile(r"^Remove (.+)$", re.I), r"Remover \1"),
    (re.compile(r"^Enable (.+)$", re.I), r"Ativar \1"),
    (re.compile(r"^Disable (.+)$", re.I), r"Desativar \1"),
    (re.compile(r"^Search (.+)$", re.I), r"Pesquisar \1"),
    (re.compile(r"^(.+) successfully$", re.I), r"\1 com sucesso"),
    (re.compile(r"^Are you sure you want to (.+)\?$", re.I), r"Tem certeza de que deseja \1?"),
]


T_CALL_RE = re.compile(
    r"\bt\(\s*(['\"])(?P<key>[^'\"]+)\1\s*,\s*(['\"])(?P<text>(?:\\.|(?!\3).)*)\3",
    re.S,
)
TRANS_RE = re.compile(
    r"<Trans[^>]+i18nKey=(['\"])(?P<key>[^'\"]+)\1[^>]+defaults=(['\"])(?P<text>(?:\\.|(?!\3).)*)\3",
    re.S,
)


def decode_js_string(value: str, quote: str = '"') -> str:
    try:
        return ast.literal_eval(quote + value + quote)
    except Exception:
        return value.replace("\\n", "\n").replace("\\'", "'").replace('\\"', '"')


def flatten_json(value: object, prefix: str = "") -> dict[str, str]:
    result: dict[str, str] = {}
    if isinstance(value, dict):
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            result.update(flatten_json(child, child_prefix))
    elif isinstance(value, str):
        result[prefix] = value
    return result


def extract_sources(source_root: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    roots = [source_root / "apps", source_root / "packages"]
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.suffix not in {".ts", ".tsx", ".js", ".jsx"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for match in T_CALL_RE.finditer(text):
                key = match.group("key")
                fallback = decode_js_string(match.group("text"), match.group(3))
                entries.setdefault(key, fallback)
            for match in TRANS_RE.finditer(text):
                key = match.group("key")
                fallback = decode_js_string(match.group("text"), match.group(3))
                entries.setdefault(key, fallback)
    return entries


def translate_by_words(text: str) -> str:
    translated = text
    for pattern, replacement in REGEX_REPLACEMENTS:
        translated = pattern.sub(replacement, translated)
    for english, portuguese in WORD_TRANSLATIONS:
        translated = re.sub(rf"\b{re.escape(english)}\b", portuguese, translated)
    translated = translated.replace(" of ", " de ")
    translated = translated.replace(" for ", " para ")
    translated = translated.replace(" with ", " com ")
    translated = translated.replace(" from ", " de ")
    translated = translated.replace(" to ", " para ")
    translated = translated.replace(" and ", " e ")
    translated = translated.replace(" or ", " ou ")
    translated = translated.replace(" the ", " ")
    translated = translated.replace(" this ", " este ")
    translated = translated.replace(" selected ", " selecionado ")
    translated = re.sub(r"\s+", " ", translated).strip()
    return translated


def translate(key: str, fallback: str, legacy_pt: dict[str, str]) -> str:
    if key in KEY_TRANSLATIONS:
        return KEY_TRANSLATIONS[key]
    if key in legacy_pt and legacy_pt[key].strip():
        return legacy_pt[key]
    if fallback in EXACT_TRANSLATIONS:
        return EXACT_TRANSLATIONS[fallback]
    if not fallback.strip():
        return fallback
    value = translate_by_words(fallback)
    if fallback.isupper() and len(fallback) > 2:
        value = value.upper()
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="../../../official-sources/carbonio-admin-console-ui")
    parser.add_argument("--legacy-pt", default="../../../official-sources/carbonio-admin-ui/translations/pt.json")
    parser.add_argument("--output", default="../translations/pt.json")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    source_root = (script_dir / args.source).resolve()
    legacy_path = (script_dir / args.legacy_pt).resolve()
    output_path = (script_dir / args.output).resolve()

    extracted = extract_sources(source_root)
    legacy_pt: dict[str, str] = {}
    if legacy_path.exists():
        legacy_pt = flatten_json(json.loads(legacy_path.read_text(encoding="utf-8")))

    result: dict[str, str] = {}
    for key, value in legacy_pt.items():
        if value.strip():
            result[key] = value

    for key, fallback in sorted(extracted.items()):
        result[key] = translate(key, fallback, legacy_pt)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    untranslated = sum(1 for key, fallback in extracted.items() if result.get(key) == fallback and fallback.strip())
    print(
        json.dumps(
            {
                "source": str(source_root),
                "keys_extracted": len(extracted),
                "keys_written": len(result),
                "untranslated_exact_fallbacks": untranslated,
                "output": str(output_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
