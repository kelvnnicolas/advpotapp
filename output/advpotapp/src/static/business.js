/* Local presentation interactions. No persistence, APIs, billing or invitations. */
(() => {
  'use strict';
  const one = (selector, root = document) => root.querySelector(selector);
  const all = (selector, root = document) => Array.from(root.querySelectorAll(selector));
  const roles = {member: 'Profissional', support: 'Apoio', admin: 'Administração do escritório'};
  const feedback = (form, text, error = false) => {
    const target = one('[data-form-feedback]', form);
    target.textContent = text;
    target.classList.toggle('is-error', error);
    target.setAttribute('role', error ? 'alert' : 'status');
  };
  const safeCell = (value) => {
    const cell = document.createElement('td');
    cell.textContent = value;
    return cell;
  };
  const teamBody = one('[data-team-body]');
  const updateTeam = () => {
    if (!teamBody) return;
    const query = one('[data-team-search]').value.trim().toLocaleLowerCase('pt-BR');
    const rows = all('[data-member-row]', teamBody);
    let visible = 0;
    rows.forEach(row => {
      row.hidden = !row.cells[0].textContent.toLocaleLowerCase('pt-BR').includes(query);
      if (!row.hidden) visible += 1;
    });
    one('[data-team-count]').textContent = `${rows.length} registros na prévia`;
    one('[data-team-empty]').hidden = visible > 0;
  };
  if (teamBody) {
    one('[data-team-search]').addEventListener('input', updateTeam);
    teamBody.addEventListener('click', event => {
      const button = event.target.closest('button');
      if (!button) return;
      const row = button.closest('[data-member-row]');
      const status = one('[data-member-status]', row);
      if (button.hasAttribute('data-discard-invite')) {
        row.remove();
        one('[data-team-feedback]').textContent = 'Convite descartado apenas nesta prévia.';
        updateTeam();
      } else if (button.hasAttribute('data-suspend-member')) {
        const suspended = row.dataset.suspended !== 'true';
        row.dataset.suspended = String(suspended);
        status.textContent = suspended ? 'Suspenso na prévia' : 'Ativo';
        status.className = `business-status ${suspended ? 'neutral' : 'positive'}`;
        button.textContent = suspended ? 'Simular reativação' : 'Simular suspensão';
        one('[data-team-feedback]').textContent = 'Situação alterada nesta tela. Nenhuma conta real foi modificada.';
      }
    });
  }

  const handlers = {
    invite(form) {
      const name = form.elements.name.value.trim();
      const email = form.elements.email.value.trim().toLowerCase();
      const role = form.elements.role.value;
      if (!Object.hasOwn(roles, role)) return feedback(form, 'Selecione um papel válido para a prévia.', true);
      if (!email.endsWith('.invalid')) return feedback(form, 'Nesta prévia, use um e-mail fictício terminado em .invalid.', true);
      if (all('[data-member-row]', teamBody).some(row => row.dataset.email.toLowerCase() === email)) {
        return feedback(form, 'Esse e-mail já existe na equipe demonstrativa.', true);
      }
      const row = document.createElement('tr');
      row.setAttribute('data-member-row', '');
      row.dataset.email = email;
      const identity = document.createElement('td');
      const title = document.createElement('strong');
      const address = document.createElement('small');
      title.textContent = name;
      address.textContent = email;
      identity.append(title, address);
      row.append(identity, safeCell(roles[role]));
      const statusCell = document.createElement('td');
      const status = document.createElement('span');
      status.className = 'business-status neutral';
      status.textContent = 'Convite não enviado';
      status.setAttribute('data-member-status', '');
      statusCell.append(status);
      const action = document.createElement('td');
      const discard = document.createElement('button');
      discard.type = 'button';
      discard.className = 'business-link-button';
      discard.setAttribute('data-discard-invite', '');
      discard.textContent = 'Descartar convite';
      action.append(discard);
      row.append(statusCell, action);
      teamBody.append(row);
      form.reset();
      updateTeam();
      feedback(form, 'Convite preparado somente nesta tela. Nenhum e-mail foi enviado e nenhum usuário foi criado.');
    },
    flow(form) {
      const name = form.elements.name.value.trim();
      const owner = form.elements.owner.value;
      if (!all('option', form.elements.owner).some(option => option.value === owner)) {
        return feedback(form, 'Selecione um responsável da equipe demonstrativa.', true);
      }
      const heading = one('[data-flow-title]');
      const before = heading.textContent;
      const version = one('[data-flow-version]');
      const nextVersion = Number(version.dataset.version || '1') + 1;
      heading.textContent = name;
      version.dataset.version = String(nextVersion);
      version.textContent = `Prévia v${nextVersion}`;
      one('[data-flow-change]').textContent = `Nome anterior: ${before}. Novo nome: ${name}. Responsável demonstrativo: ${owner}. As seis etapas foram preservadas.`;
      feedback(form, 'Configuração aplicada apenas nesta visualização. Nenhuma demanda ou versão real foi alterada.');
    },
    settings(form) {
      const email = form.elements.email.value.trim().toLowerCase();
      if (!email.endsWith('.invalid')) return feedback(form, 'Use um canal fictício terminado em .invalid nesta prévia.', true);
      one('[data-settings-name]').textContent = form.elements.name.value.trim();
      one('[data-settings-timezone]').textContent = 'America/Sao_Paulo';
      one('[data-settings-email]').textContent = email;
      feedback(form, 'Resumo atualizado nesta tela. A configuração do sistema permanece inalterada.');
    },
    contract(form) {
      one('[data-contract-name]').textContent = form.elements.name.value.trim();
      one('[data-contract-owner]').textContent = form.elements.owner.value.trim();
      const summary = one('[data-contract-summary]');
      summary.hidden = false;
      feedback(form, 'Resumo preparado. Nenhum escritório, checkout ou pagamento foi criado.');
      summary.focus();
    },
  };

  all('[data-preview-form]').forEach(form => {
    // Install the no-submit guard before enabling controls. No action submits data.
    form.addEventListener('submit', event => event.preventDefault());
    const handle = handlers[form.dataset.previewForm];
    if (!handle) return;
    const run = () => {
      all('input[required]:not([type=checkbox])', form).forEach(input => {
        input.setCustomValidity(input.value.trim() ? '' : 'Preencha este campo com dados fictícios.');
      });
      if (!form.reportValidity()) return;
      handle(form);
    };
    form.addEventListener('input', event => {
      if (event.target instanceof HTMLInputElement) event.target.setCustomValidity('');
    });
    one('[data-preview-save]', form).addEventListener('click', run);
    form.addEventListener('keydown', event => {
      if (event.key === 'Enter' && event.target.matches('input:not([type=checkbox])')) {
        event.preventDefault();
        run();
      }
    });
    one('fieldset', form).disabled = false;
    form.dataset.previewReady = 'true';
  });
})();
