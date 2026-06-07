(function () {
  "use strict";

  if (window.__carbonioCustomPtbrVisualI18nLoaded) {
    return;
  }
  window.__carbonioCustomPtbrVisualI18nLoaded = true;

  var replacements = [
    ["Allow searching users' information in all domains", "Permitir pesquisa de informações de usuários em todos os domínios"],
    ["Only allow outbound disclaimers", "Permitir avisos legais apenas em mensagens de saída"],
    ["Domain System Notifications", "Notificações do sistema do domínio"],
    ["Notification Sender", "Remetente da notificação"],
    ["Send notifications to...", "Enviar notificações para..."],
    ["General", "GERAL"],
    ["Profile", "PERFIL"],
    ["Configuration", "CONFIGURAÇÃO"],
    ["Security", "SEGURANÇA"],
    ["Administration", "ADMINISTRAÇÃO"],
    ["Phone", "Telefone"],
    ["Home", "Residencial"],
    ["Mobile", "Celular"],
    ["Pager", "Bip"],
    ["Fax Number", "Número de fax"],
    ["Company", "Empresa"],
    ["Job Title", "Cargo"],
    ["Country", "País"],
    ["State", "Estado"],
    ["City", "Cidade"],
    ["Postal Code", "CEP"],
    ["System account for Non-Spam (Ham) training.", "Conta de sistema para treinamento de não spam (Ham)."],
    ["System account for spam training.", "Conta de sistema para treinamento de spam."],
    ["System account for Anti-virus quarantine.", "Conta de sistema para quarentena antivírus."],
    ["DelegatedAdmin", "Administrador delegado"],
    ["Locked", "Bloqueado"],
    ["Unlimited", "Ilimitado"],
    ["System", "Sistema"],
    ["Sunday", "Domingo"],
    ["Monday", "Segunda-feira"],
    ["Tuesday", "Terça-feira"],
    ["Wednesday", "Quarta-feira"],
    ["Thursday", "Quinta-feira"],
    ["Friday", "Sexta-feira"],
    ["Saturday", "Sábado"],
    ["January", "Janeiro"],
    ["February", "Fevereiro"],
    ["March", "Março"],
    ["April", "Abril"],
    ["May", "Maio"],
    ["June", "Junho"],
    ["July", "Julho"],
    ["August", "Agosto"],
    ["September", "Setembro"],
    ["October", "Outubro"],
    ["November", "Novembro"],
    ["December", "Dezembro"],
    ["Jan", "Jan"],
    ["Feb", "Fev"],
    ["Mar", "Mar"],
    ["Apr", "Abr"],
    ["May", "Mai"],
    ["Jun", "Jun"],
    ["Jul", "Jul"],
    ["Aug", "Ago"],
    ["Sep", "Set"],
    ["Oct", "Out"],
    ["Nov", "Nov"],
    ["Dec", "Dez"]
  ];

  var blockTags = {
    SCRIPT: true,
    STYLE: true,
    TEXTAREA: true,
    INPUT: true,
    SELECT: true,
    OPTION: true,
    CODE: true,
    PRE: true
  };

  function escapeRegExp(value) {
    return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  function isBreadcrumbHomeNode(node) {
    var text = (node.nodeValue || "").trim();
    if (text !== "Home" && text !== "Residencial") {
      return false;
    }
    var element = node.parentElement;
    for (var i = 0; element && i < 6; i += 1) {
      var content = element.textContent || "";
      if (/^\s*(Home|Residencial)\s*\/\s*/.test(content)) {
        return true;
      }
      element = element.parentElement;
    }
    return false;
  }

  function translateText(value) {
    var next = value;
    for (var i = 0; i < replacements.length; i += 1) {
      var from = replacements[i][0];
      var to = replacements[i][1];
      var prefix = /^\w/.test(from) ? "\\b" : "";
      var suffix = /\w$/.test(from) ? "\\b" : "";
      next = next.replace(new RegExp(prefix + escapeRegExp(from) + suffix, "g"), to);
    }
    return next;
  }

  function shouldSkip(node) {
    var parent = node && node.parentElement;
    return !parent || blockTags[parent.tagName] || parent.closest("[data-ptbr-visual-i18n-skip]");
  }

  function translateNode(node) {
    if (!node || node.nodeType !== Node.TEXT_NODE || shouldSkip(node)) {
      return;
    }
    var original = node.nodeValue || "";
    if (isBreadcrumbHomeNode(node)) {
      node.nodeValue = original.replace(/\b(Home|Residencial)\b/g, "Início");
      return;
    }
    var translated = translateText(original);
    if (translated !== original) {
      node.nodeValue = translated;
    }
  }

  function walk(root) {
    if (!root) {
      return;
    }
    if (root.nodeType === Node.TEXT_NODE) {
      translateNode(root);
      return;
    }
    if (root.nodeType !== Node.ELEMENT_NODE && root.nodeType !== Node.DOCUMENT_NODE) {
      return;
    }
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    var node = walker.nextNode();
    while (node) {
      translateNode(node);
      node = walker.nextNode();
    }
  }

  function scheduleWalk(root) {
    window.requestAnimationFrame(function () {
      walk(root || document.body);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      scheduleWalk(document.body);
    });
  } else {
    scheduleWalk(document.body);
  }

  var observer = new MutationObserver(function (mutations) {
    for (var i = 0; i < mutations.length; i += 1) {
      var mutation = mutations[i];
      if (mutation.type === "characterData") {
        translateNode(mutation.target);
      } else if (mutation.type === "childList") {
        for (var j = 0; j < mutation.addedNodes.length; j += 1) {
          scheduleWalk(mutation.addedNodes[j]);
        }
      }
    }
  });

  observer.observe(document.documentElement, {
    childList: true,
    characterData: true,
    subtree: true
  });
})();
