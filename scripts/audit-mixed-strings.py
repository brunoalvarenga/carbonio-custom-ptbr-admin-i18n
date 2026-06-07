#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = ROOT / "translations" / "pt.json"

CRITICAL_TRANSLATIONS = {
    "label.account_password_setting_note_for_external_authentication": "As configurações abaixo não afetam senhas definidas por usuários em domínios configurados para autenticação externa. As alterações feitas aqui substituirão as configurações de COS para senha e bloqueio por falhas de login.",
    "cos.prevent_user_from_changing_password": "Impedir que o usuário altere a senha",
    "cos.enable_past_due_reminders": "Ativar lembretes de compromissos vencidos",
    "cos.preferences.allowTheUserToAskForAReadReceipt": "Permitir que o usuário solicite confirmação de leitura",
    "cos.add_invites_with_publish_method": "Adicionar convites com método PUBLISH",
    "cos.use_ical_delegation_model_for_shared_calendars": "Usar modelo de delegação iCal para calendários compartilhados",
    "cos.save_to_Sent": "Salvar em enviados",
    "cos.session_idle_timeout": "Tempo limite de sessão ociosa",
    "cos.enable_auto_add_contacts": "Ativar adição automática de contatos",
    "cos.use_gal_to_auto_fill": "Usar GAL para preenchimento automático",
    "cos.default_view.work_week": "Visualização de semana útil",
    "label.receiving_mails": "Recebimento de e-mails",
    "label.sending_mails": "Envio de e-mails",
    "label.contact_options": "Opções de contato",
    "label.calendar_options": "Opções de calendário",
    "label.the_week_starts_on": "A semana começa em",
    "label.default_appointment_visibility": "Visibilidade padrão dos compromissos",
    "label.add_appointments_when_invited": "Adicionar automaticamente compromissos quando o usuário for convidado",
    "quarantine.delete_and_recreate_quarantine": "EXCLUIR E RECRIAR CONTA DE QUARENTENA",
    "quarantine.to_make_changes_restart_the_MTA": "Para efetivar as alterações, reinicie o MTA.",
    "quarantine.refresh_list": "ATUALIZAR LISTA",
    "wsc.section.content.description.enableFeature": "Ativar mensagens, chats em grupo, chamadas de vídeo e compartilhamento de arquivos.",
    "wsc.section.content.toggle.createPrivate": "Usuários podem iniciar chats privados",
    "wsc.section.content.toggle.createGroup": "Usuários podem criar chats em grupo",
    "wsc.section.header.title.chats": "Chats privados e em grupo",
    "wsc.section.header.title.attachments": "Compartilhamento e anexos",
    "domain.account_list": "Lista de contas",
    "domain.accounts.totalAccounts": "Total de contas",
    "domain.globalSettings.allowSearchUserFromAllDomains": "Permitir pesquisa de informações de usuários em todos os domínios",
    "backup.tuning_options": "Opções de ajuste",
    "cos.general_options": "Opções gerais",
    "label.administration": "ADMINISTRAÇÃO",
    "label.administrators": "Administradores",
    "label.active_sessions": "Sessões ativas",
    "label.can_access_settings": "Pode acessar as configurações",
    "label.city": "Cidade",
    "label.company": "Empresa",
    "label.configuration": "CONFIGURAÇÃO",
    "label.country": "País",
    "label.Cos_list": "Lista de COS",
    "label.cos_list": "Lista de COS",
    "label.creation_date": "Data de criação",
    "label.disclaimer": "Aviso legal",
    "label.domain_system_notifications": "Notificações do sistema do domínio",
    "label.enable_disclaimers_for_all_domains": "Aviso legal obrigatório para todos os domínios",
    "label.end_session": "ENCERRAR SESSÃO",
    "label.fax_number": "Número de fax",
    "label.general": "GERAL",
    "label.forgotten_password": "Senha esquecida",
    "label.general_options": "Opções gerais",
    "label.home": "Residencial",
    "label.i_am_looking_for_this_account": "Buscar conta...",
    "label.i_am_looking_for_this_domain": "Buscar domínio...",
    "label.i_m_looking_for_the_session": "Buscar sessão...",
    "label.job_title": "Cargo",
    "label.mailbox_quota_limit_gb": "Limite de cota da caixa postal (GB)",
    "label.mailing_options": "Opções de e-mail",
    "label.mobile": "Celular",
    "label.not_set": "Não definido",
    "label.notes": "Observações",
    "label.one_time_password_management": "Gerenciamento de senha de uso único (OTP)",
    "label.only_allow_outbound_disclaimers": "Permitir avisos legais apenas em mensagens de saída",
    "label.pager": "Bip",
    "label.password_and_repeat_password_not_match": "As senhas não coincidem",
    "label.password_length_msg": "A senha deve ter mais de 5 caracteres",
    "label.phone": "Telefone",
    "label.postal_code": "CEP",
    "label.profile": "PERFIL",
    "label.scroll_down_to_view_other_items": "Role para baixo para ver outros itens",
    "label.security": "SEGURANÇA",
    "label.session_id": "ID da sessão",
    "label.state": "Estado",
    "label.what_is_a_gal": "O que é GAL?",
    "mta.outbound_flow": "Fluxo de saída",
}

FORBIDDEN_PATTERNS = [
    r"\bPrevent user\b",
    r"\bActivate para\b",
    r"\bPermitir users\b",
    r"\bUsuários can\b",
    r"\bREFRESH LIST\b",
    r"\bThe Week starts on\b",
    r"\bDefault Appointment\b",
    r"\bAppointment Reminder\b",
    r"\bAutomatically add\b",
    r"\bShow read receipts\b",
    r"\bMaximum number de\b",
    r"\bMinimum password\b",
    r"\bRead Receipt settings\b",
    r"\bForwarding\b",
    r"\bQUARANTINE ACCOUNT\b",
    r"\bTo make changes effective\b",
    r"\bfailed login lockout\b",
    r"\bMaximum attachment size\b",
    r"\bPrivate e Grupo Chats\b",
    r"\bSharing & Anexos\b",
    r"\bReceiving Mails\b",
    r"\bSending Mails\b",
    r"\bSalvar para sent\b",
    r"\bContato Options\b",
    r"\bauto-add contacts\b",
    r"\bUse GAL para auto-fill\b",
    r"\bCalendário Options\b",
    r"\bWork Week Visualizar\b",
    r"\bOutbound Flow\b",
    r"\bAccounts List\b",
    r"\bTotal Accounts\b",
    r"\bI'm looking for this account\b",
    r"\bI'm looking for this domain\b",
    r"\bCreation Date\b",
    r"\bNot Set\b",
    r"\bNotes\b",
    r"\bHandle Contas\b",
    r"\bCos Lista\b",
    r"\bMailbox Quota Limit\b",
    r"\bCota Limit\b",
    r"\bActive Sessions\b",
    r"\bSession ID\b",
    r"\bEND SESSION\b",
    r"\bScroll down para view\b",
    r"\bAllow searching users\b",
    r"\bDomínio System Notificações\b",
    r"\bDisclaimer obrigatório\b",
    r"\bdisclaimers apenas\b",
    r"\bAdministrators\b",
    r"\bGENERAL\b",
    r"\bPROFILE\b",
    r"\bCONFIGURATION\b",
    r"\bSECURITY\b",
    r"\bADMINISTRATION\b",
    r"\bFax Number\b",
    r"\bJob Title\b",
    r"\bPostal Code\b",
    r"\bPhone\b",
    r"\bCompany\b",
    r"\bCountry\b",
    r"\bState\b",
    r"\bCity\b",
    r"\bMobile\b",
    r"\bTuning Options\b",
    r"\bGeral Options\b",
    r"\bCan access Configurações\b",
    r"\bForgotten Senha\b",
    r"\bE-mail Options\b",
    r"\bOne Hora Senha management\b",
    r"\bPasswords do not match\b",
    r"\bSenha should be\b",
]


def main() -> int:
    data = json.loads(TRANSLATIONS.read_text(encoding="utf-8"))
    errors: list[str] = []

    for key, expected in CRITICAL_TRANSLATIONS.items():
        actual = data.get(key)
        if actual != expected:
            errors.append(f"{key}: esperado {expected!r}, obtido {actual!r}")

    compiled = [re.compile(pattern, re.I) for pattern in FORBIDDEN_PATTERNS]
    for key, value in data.items():
        if not isinstance(value, str):
            continue
        for pattern in compiled:
            if pattern.search(value):
                errors.append(f"{key}: frase hibrida proibida: {value!r}")
                break

    if errors:
        print("Falha na auditoria PT-BR:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"auditoria PT-BR ok: {len(CRITICAL_TRANSLATIONS)} chaves criticas verificadas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
