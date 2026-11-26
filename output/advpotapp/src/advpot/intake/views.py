from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from . import access, forms, services, workflow
from .exceptions import WorkflowConflict
from .models import Contact, ContactEvent, Demand, DemandEvent, DemandGrant, CommercialHandoff


def failure(form, error):
    for message in error.messages if isinstance(error, ValidationError) else [str(error)]:
        form.add_error(None, message)
    return 409 if isinstance(error, WorkflowConflict) else 200


def page(request, queryset):
    return Paginator(queryset, 20).get_page(request.GET.get('page'))


@login_required
def contacts(request):
    records = access.visible_contacts(request.user)
    query = request.GET.get('q', '').strip()[:150]
    if query:
        records = records.filter(Q(name__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query))
    return render(request, 'intake/contacts.html', {'page_obj': page(request, records), 'query': query, 'can_create': access.can_create(request.user)})


@login_required
def contact_form(request, pk=None):
    if not access.can_create(request.user):
        raise PermissionDenied
    contact = get_object_or_404(access.visible_contacts(request.user, 'edit'), pk=pk) if pk else None
    form = forms.ContactForm(request.POST or None, instance=contact)
    status, duplicates = 200, []
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        matches = access.possible_duplicates(request.user, name=data['name'], email=data['email'], phone=data['phone'])
        if contact:
            matches = matches.exclude(pk=contact.pk)
        else:
            matches = matches.exclude(creation_key=data['operation_key'])
        duplicates = list(matches[:10])
        if duplicates and not data['duplicate_ack']:
            form.add_error('duplicate_ack', 'Confira os cadastros semelhantes antes de continuar.')
        else:
            try:
                if contact:
                    result = services.update_contact(actor=request.user, contact_id=contact.pk, expected_version=data['expected_version'], data=data)
                else:
                    result = services.create_contact(actor=request.user, operation_key=data['operation_key'], data=data)
                messages.success(request, 'Cadastro salvo.')
                return redirect('contact-detail', pk=result.pk)
            except (ValidationError, WorkflowConflict) as error:
                status = failure(form, error)
    return render(request, 'intake/form.html', {'form': form, 'heading': 'Editar cliente / contato' if pk else 'Novo cliente / contato', 'duplicates': duplicates, 'back_url': '/clientes/'}, status=status)


@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(access.visible_contacts(request.user), pk=pk)
    history = ContactEvent.objects.filter(contact=contact).select_related('actor')[:50] if access.visible_contacts(request.user, 'view_history').filter(pk=pk).exists() else None
    return render(request, 'intake/contact_detail.html', {'contact': contact, 'can_edit': access.visible_contacts(request.user, 'edit').filter(pk=pk).exists(), 'history': history, 'demands': access.visible_demands(request.user).filter(contact=contact)[:20]})


@login_required
def demands(request):
    records = access.visible_demands(request.user).select_related('responsible')
    query = request.GET.get('q', '').strip()[:180]
    if query:
        records = records.filter(Q(title__icontains=query) | Q(need__icontains=query) | Q(origin__icontains=query))
    status = request.GET.get('status', 'open')
    if status in Demand.Status.values:
        records = records.filter(status=status)
    else:
        status = 'all'
    stage = request.GET.get('stage', '')
    if stage in Demand.Stage.values:
        records = records.filter(commercial_stage=stage)
    current_page = page(request, records)
    columns = [{'label': label, 'records': [item for item in current_page.object_list if item.commercial_stage == value]} for value, label in Demand.Stage.choices]
    return render(request, 'intake/demands.html', {'page_obj': current_page, 'columns': columns, 'query': query, 'selected_status': status, 'selected_stage': stage, 'statuses': Demand.Status.choices, 'stages': Demand.Stage.choices, 'board': request.GET.get('view') == 'board', 'can_create': access.can_create(request.user)})


@login_required
def demand_create(request):
    if not access.can_create(request.user):
        raise PermissionDenied
    form = forms.DemandCreateForm(request.POST or None, actor=request.user)
    status = 200
    if request.method == 'POST' and form.is_valid():
        try:
            demand = services.create_demand(actor=request.user, operation_key=form.cleaned_data['operation_key'], data=form.cleaned_data)
            return redirect('demand-detail', pk=demand.pk)
        except (ValidationError, WorkflowConflict) as error:
            status = failure(form, error)
    return render(request, 'intake/form.html', {'form': form, 'heading': 'Novo atendimento', 'back_url': '/atendimentos/', 'contact_hint': True}, status=status)


@login_required
def demand_edit(request, pk):
    demand = get_object_or_404(access.visible_demands(request.user), pk=pk)
    action = 'edit_intake' if demand.journey_stage == 'reception' else 'manage_opportunity'
    if not access.visible_demands(request.user, action).filter(pk=pk).exists() or demand.responsible_id != request.user.pk:
        raise PermissionDenied
    form = forms.DemandEditForm(request.POST or None, instance=demand)
    status = 200
    if request.method == 'POST' and form.is_valid():
        try:
            workflow.update_demand(actor=request.user, demand_id=pk, expected_version=form.cleaned_data['expected_version'], operation_key=form.cleaned_data['operation_key'], data={key: value for key, value in form.cleaned_data.items() if key not in {'expected_version', 'operation_key'}})
            return redirect('demand-detail', pk=pk)
        except (ValidationError, WorkflowConflict) as error:
            status = failure(form, error)
    return render(request, 'intake/form.html', {'form': form, 'heading': 'Atualizar atendimento', 'back_url': f'/atendimentos/{pk}/'}, status=status)


@login_required
def demand_detail(request, pk):
    demand = get_object_or_404(access.visible_demands(request.user).select_related('responsible', 'recovery_queue'), pk=pk)
    contact = access.visible_contacts(request.user).filter(pk=demand.contact_id).first()
    owned = demand.responsible_id == request.user.pk and demand.status == 'open'
    pending = CommercialHandoff.objects.filter(demand=demand, state='pending').select_related('target').first()
    action = 'edit_intake' if demand.journey_stage == 'reception' else 'manage_opportunity'
    allowed = lambda permission: access.visible_demands(request.user, permission).filter(pk=pk).exists()
    initial = {'expected_version': demand.version}
    return render(request, 'intake/demand_detail.html', {
        'demand': demand, 'contact': contact, 'pending': pending,
        'can_edit': owned and not pending and allowed(action),
        'can_manage_access': allowed('manage_access'),
        'stage_form': forms.StageForm(initial=initial) if owned and not pending and demand.journey_stage == 'commercial' and allowed('manage_opportunity') else None,
        'send_form': forms.SendHandoffForm(demand=demand, initial=initial) if owned and not pending and demand.journey_stage == 'reception' and allowed('send_handoff') else None,
        'cancel_form': forms.CancelHandoffForm(initial=initial) if owned and pending and allowed('send_handoff') else None,
        'history': DemandEvent.objects.filter(demand=demand).select_related('actor')[:50] if allowed('view_history') else None,
    })


def command_response(request, form, callback, *, back):
    status = 200
    if form.is_valid():
        try:
            callback(form.cleaned_data)
            messages.success(request, 'Operação registrada.')
            return redirect(back)
        except (ValidationError, WorkflowConflict) as error:
            status = failure(form, error)
    return render(request, 'intake/form.html', {'form': form, 'heading': 'Revisar operação', 'back_url': back}, status=status)


@login_required
@require_POST
def demand_stage(request, pk):
    return command_response(request, forms.StageForm(request.POST), lambda data: workflow.move_commercial_stage(actor=request.user, demand_id=pk, **data), back=f'/atendimentos/{pk}/')


@login_required
@require_POST
def handoff_send(request, pk):
    demand = get_object_or_404(access.visible_demands(request.user, 'send_handoff'), pk=pk)
    return command_response(request, forms.SendHandoffForm(request.POST, demand=demand), lambda data: workflow.send_to_commercial(actor=request.user, demand_id=pk, target_id=data['target'].pk, expected_version=data['expected_version'], operation_key=data['operation_key']), back=f'/atendimentos/{pk}/')


@login_required
@require_POST
def handoff_cancel(request, pk):
    return command_response(request, forms.CancelHandoffForm(request.POST), lambda data: workflow.cancel_handoff(actor=request.user, demand_id=pk, **data), back=f'/atendimentos/{pk}/')


@login_required
def handoffs(request):
    records = CommercialHandoff.objects.filter(target=request.user, state='pending', demand_id__in=DemandGrant.objects.filter(user=request.user, action='receive_handoff').values('demand_id')).select_related('demand') if 'commercial' in access.departments(request.user) else CommercialHandoff.objects.none()
    current_page = page(request, records)
    items = []
    for handoff in current_page.object_list:
        readable = access.visible_demands(request.user).filter(pk=handoff.demand_id).exists()
        items.append({'id': handoff.pk, 'demand_id': handoff.demand_id, 'title': handoff.demand.title if readable else None, 'blocked': handoff.blocked, 'can_receive': readable and not handoff.blocked and access.visible_demands(request.user, 'manage_opportunity').filter(pk=handoff.demand_id).exists(), 'form': forms.DecisionForm(initial={'expected_version': handoff.demand.version})})
    return render(request, 'intake/handoffs.html', {'items': items, 'page_obj': current_page})


@login_required
@require_POST
def handoff_decide(request, pk):
    def decide(data):
        callback = workflow.accept_handoff if data.pop('decision') == 'accept' else workflow.return_handoff
        if callback == workflow.accept_handoff:
            data.pop('reason')
        callback(actor=request.user, handoff_id=pk, **data)
    return command_response(request, forms.DecisionForm(request.POST), decide, back='/passagens/')


@login_required
def business_access(request):
    if not access.is_authority(request.user):
        raise PermissionDenied
    form = forms.BusinessAccessForm(request.POST or None)
    if request.method == 'POST':
        def apply(data):
            args = {'actor': request.user, 'target': data['target'], 'enabled': data['enabled']}
            if data['kind'] == 'department':
                services.assign_department(**args, department=data['department'])
            elif data['kind'] == 'contact':
                services.grant_contact_action(**args, contact_id=data['record_id'], action=data['action'])
            else:
                services.grant_demand_action(**args, demand_id=data['record_id'], action=data['action'])
        return command_response(request, form, apply, back='/gestao/acessos-negocio/')
    return render(request, 'intake/form.html', {'form': form, 'heading': 'Acessos de negócio', 'back_url': '/meu-trabalho/', 'access_hint': True})


@login_required
def recovery(request):
    if not access.is_authority(request.user) and 'management' not in access.departments(request.user):
        raise PermissionDenied
    records = access.recoverable_demands(request.user)
    current_page = page(request, records)
    items = [{'id': item.pk, 'stage': item.get_journey_stage_display(), 'form': forms.RecoveryForm(demand=item, initial={'expected_version': item.version})} for item in current_page.object_list]
    return render(request, 'intake/recovery.html', {'items': items, 'page_obj': current_page})


@login_required
@require_POST
def recover(request, pk):
    if not access.is_authority(request.user) and 'management' not in access.departments(request.user):
        raise PermissionDenied
    demand = get_object_or_404(access.recoverable_demands(request.user), pk=pk)
    return command_response(request, forms.RecoveryForm(request.POST, demand=demand), lambda data: workflow.recover_demand(actor=request.user, demand_id=pk, target_id=data['target'].pk, expected_version=data['expected_version'], operation_key=data['operation_key']), back='/gestao/recuperacao/')


@login_required
def demand_access(request, pk):
    demand = get_object_or_404(access.visible_demands(request.user, 'manage_access'), pk=pk)
    form = forms.DelegatedAccessForm(request.POST or None, actor=request.user, demand=demand)
    if request.method == 'POST':
        return command_response(request, form, lambda data: services.grant_demand_action(actor=request.user, target=data['target'], demand_id=pk, action=data['action'], enabled=data['enabled']), back=f'/atendimentos/{pk}/acessos/')
    return render(request, 'intake/form.html', {'form': form, 'heading': 'Acessos desta demanda', 'back_url': f'/atendimentos/{pk}/'})
