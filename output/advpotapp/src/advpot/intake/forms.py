import uuid
from django import forms
from advpot.identity.models import User
from . import access
from .models import BusinessAssignment, Contact, ContactGrant, Demand, DemandGrant


class ContactForm(forms.ModelForm):
    operation_key = forms.UUIDField(widget=forms.HiddenInput, initial=uuid.uuid4, required=False)
    expected_version = forms.IntegerField(widget=forms.HiddenInput, required=False)
    duplicate_ack = forms.BooleanField(label='Revisei os possíveis cadastros semelhantes e desejo manter este cadastro.', required=False)

    class Meta:
        model = Contact
        fields = ['kind', 'name', 'email', 'phone', 'channel_absence_reason']
        widgets = {'channel_absence_reason': forms.Textarea(attrs={'rows': 2})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and not self.instance._state.adding:
            self.fields['expected_version'].required = True
            self.initial['expected_version'] = self.instance.version
        else:
            self.fields['operation_key'].required = True


class DemandCreateForm(forms.ModelForm):
    operation_key = forms.UUIDField(widget=forms.HiddenInput, initial=uuid.uuid4)

    class Meta:
        model = Demand
        fields = ['contact', 'title', 'need', 'origin', 'area', 'next_step', 'next_step_on']
        labels = {'contact': 'Contato'}
        widgets = {'need': forms.Textarea(attrs={'rows': 4}), 'next_step_on': forms.DateInput(attrs={'type': 'date'})}
        help_texts = {'area': 'Pode ficar em branco enquanto a área é classificada.', 'next_step_on': 'Data combinada de acompanhamento. Não é prazo fatal.'}

    def __init__(self, *args, actor, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact'].queryset = access.visible_contacts(actor)
        self.fields['contact'].label_from_instance = lambda contact: contact.name


class DemandEditForm(forms.ModelForm):
    operation_key = forms.UUIDField(widget=forms.HiddenInput, initial=uuid.uuid4)
    expected_version = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Demand
        fields = ['title', 'need', 'origin', 'area', 'next_step', 'next_step_on', 'solution', 'proposal']
        widgets = {field: forms.Textarea(attrs={'rows': 3}) for field in ['need', 'solution', 'proposal']}
        help_texts = {'proposal': 'Resumo comercial. Não formaliza contrato, recebimento ou liberação financeira.'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['expected_version'] = self.instance.version
        self.fields['next_step_on'].widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        if self.instance.journey_stage == 'commercial':
            for field in ['title', 'need', 'origin', 'area']:
                self.fields.pop(field)


class VersionedForm(forms.Form):
    expected_version = forms.IntegerField(widget=forms.HiddenInput)
    operation_key = forms.UUIDField(widget=forms.HiddenInput, initial=uuid.uuid4)


class StageForm(VersionedForm):
    stage = forms.ChoiceField(label='Próxima situação', choices=[('proposal', 'Proposta'), ('formalization', 'Preparar formalização'), ('lost', 'Perdida'), ('cancelled', 'Cancelada')])
    reason = forms.CharField(label='Motivo da perda/cancelamento', required=False, max_length=500, widget=forms.Textarea(attrs={'rows': 2}))


class SendHandoffForm(VersionedForm):
    target = forms.ModelChoiceField(label='Destinatário do Comercial', queryset=User.objects.none())

    def __init__(self, *args, demand, **kwargs):
        super().__init__(*args, **kwargs)
        candidates = User.objects.filter(is_active=True, pk__in=BusinessAssignment.objects.filter(department='commercial').values('user_id'))
        for action in ['view', 'receive_handoff', 'manage_opportunity']:
            candidates = candidates.filter(pk__in=DemandGrant.objects.filter(demand=demand, action=action).values('user_id'))
        self.fields['target'].queryset = candidates.order_by('username')


class DecisionForm(VersionedForm):
    decision = forms.ChoiceField(choices=[('accept', 'Aceitar'), ('return', 'Devolver')])
    reason = forms.CharField(required=False, max_length=500, label='Motivo da devolução')


class CancelHandoffForm(VersionedForm):
    reason = forms.CharField(max_length=500, label='Motivo do cancelamento')


class BusinessAccessForm(forms.Form):
    kind = forms.ChoiceField(label='Tipo de concessão', choices=[('department', 'Setor'), ('contact', 'Acesso a contato'), ('demand', 'Acesso a demanda')])
    target = forms.ModelChoiceField(label='Usuário ativo', queryset=User.objects.filter(is_active=True).order_by('username'))
    department = forms.ChoiceField(label='Setor', choices=[('', 'Selecione para atribuição de setor'), *BusinessAssignment.Department.choices], required=False)
    record_id = forms.UUIDField(label='Referência completa do registro', required=False)
    action = forms.ChoiceField(label='Ação no registro', choices=[('', 'Selecione para acesso ao registro'), *dict([*ContactGrant.Action.choices, *DemandGrant.Action.choices]).items()], required=False)
    enabled = forms.BooleanField(label='Conceder (desmarque para revogar)', required=False, initial=True)

    def clean(self):
        data = super().clean()
        kind = data.get('kind')
        if kind == 'department' and not data.get('department'):
            self.add_error('department', 'Selecione o setor.')
        if kind in {'contact', 'demand'}:
            if not data.get('record_id'):
                self.add_error('record_id', 'Informe a referência do registro.')
            valid = ContactGrant.Action.values if kind == 'contact' else DemandGrant.Action.values
            if data.get('action') not in valid:
                self.add_error('action', 'Selecione uma ação válida para este tipo de registro.')
        return data


class RecoveryForm(VersionedForm):
    target = forms.ModelChoiceField(label='Novo responsável', queryset=User.objects.filter(is_active=True).order_by('username'))
