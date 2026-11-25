from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_POST
from .forms import InternalAuthenticationForm
from .models import User
from .throttling import reserve_attempt, clear_account_attempts
from .forms import InternalUserCreationForm, InternalUserEditForm
from .services import create_internal_user, update_internal_user, revoke_sessions


@method_decorator(sensitive_post_parameters('password'), name='dispatch')
class InternalLoginView(LoginView):
    template_name = 'identity/login.html'
    authentication_form = InternalAuthenticationForm
    redirect_authenticated_user = True

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '').strip()[:150]
        if not reserve_attempt(request, username):
            form = self.get_form_class()(request=request, data={'username': username, 'password': ''})
            form.is_valid()
            form.add_error(None, 'Aguarde 15 minutos antes de tentar novamente ou procure o administrador.')
            response = self.render_to_response(self.get_context_data(form=form), status=429)
            response['Retry-After'] = '900'
            return response
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        clear_account_attempts(form.cleaned_data['username'])
        return super().form_valid(form)


class InternalLogoutView(LogoutView):
    pass


@never_cache
@login_required
def dashboard(request):
    from advpot.cases.queries import visible_cases
    return render(request, 'identity/dashboard.html', {'case_count': visible_cases(request.user).count()})


@never_cache
@login_required
def users(request):
    if not request.user.can_manage_identity:
        raise PermissionDenied
    query = request.GET.get('q', '').strip()[:150]
    queryset = User.objects.order_by('username')
    if query:
        queryset = queryset.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
    page = Paginator(queryset, 20).get_page(request.GET.get('page'))
    return render(request, 'identity/users.html', {'page_obj': page, 'q': query})


@never_cache
@login_required
@sensitive_post_parameters('password1', 'password2')
def user_create(request):
    if not request.user.can_manage_identity:
        raise PermissionDenied
    form = InternalUserCreationForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        try:
            create_internal_user(actor=request.user, form=form)
        except ValidationError as error:
            for field, errors in error.message_dict.items():
                form.add_error(field, errors)
        else:
            messages.success(request, 'Usuário criado. O acesso aos casos deve ser concedido separadamente.')
            return redirect('users')
    return render(request, 'identity/user_form.html', {'form': form})


@never_cache
@login_required
def user_edit(request, pk):
    if not request.user.can_manage_identity:
        raise PermissionDenied
    account = get_object_or_404(User, pk=pk)
    form = InternalUserEditForm(request.POST if request.method == 'POST' else None, instance=account, actor=request.user)
    if request.method == 'POST' and form.is_valid():
        update_internal_user(actor=request.user, user_id=pk, changes=form.cleaned_data)
        messages.success(request, 'Usuário atualizado. Alterações de perfil ou situação revogam as sessões anteriores.')
        return redirect('users')
    return render(request, 'identity/user_form.html', {'form': form, 'account': account})


@never_cache
@login_required
@require_POST
def user_revoke(request, pk):
    if not request.user.can_manage_identity:
        raise PermissionDenied
    get_object_or_404(User, pk=pk)
    revoke_sessions(actor=request.user, user_id=pk)
    messages.success(request, 'Sessões revogadas. Um novo login será necessário.')
    return redirect('users')
