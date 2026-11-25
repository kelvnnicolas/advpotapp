from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import User


class InternalAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Usuário', max_length=150, widget=forms.TextInput(attrs={'autocomplete': 'username', 'autofocus': True}))
    password = forms.CharField(label='Senha', strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
    error_messages = {
        'invalid_login': 'Não foi possível entrar. Confira seus dados ou procure o administrador.',
        'inactive': 'Não foi possível entrar. Confira seus dados ou procure o administrador.',
    }


class InternalUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'role']
        labels = {'role': 'Perfil'}


class InternalUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'role', 'is_active']
        labels = {'role': 'Perfil', 'is_active': 'Acesso ativo'}

    def __init__(self, *args, actor, **kwargs):
        self.actor = actor
        super().__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()
        if self.instance.pk == self.actor.pk and (
            not data.get('is_active') or data.get('role') != User.Role.ACCESS_ADMIN
        ):
            raise forms.ValidationError('Você não pode desativar nem remover seu próprio perfil de administração.')
        return data
