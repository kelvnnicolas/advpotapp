from django.urls import include, path
from django.views.generic import RedirectView
from advpot.identity import views as identity
from advpot.cases import views as cases
from advpot.audit.views import history
from advpot.intake import views as intake

urlpatterns = [
    path('', include('advpot.business_frontend.urls')),
    path('clientes/', intake.contacts, name='contacts'),
    path('clientes/novo/', intake.contact_form, name='contact-create'),
    path('clientes/<uuid:pk>/', intake.contact_detail, name='contact-detail'),
    path('clientes/<uuid:pk>/editar/', intake.contact_form, name='contact-edit'),
    path('atendimentos/', intake.demands, name='demands'),
    path('atendimentos/novo/', intake.demand_create, name='demand-create'),
    path('atendimentos/<uuid:pk>/', intake.demand_detail, name='demand-detail'),
    path('atendimentos/<uuid:pk>/editar/', intake.demand_edit, name='demand-edit'),
    path('atendimentos/<uuid:pk>/acessos/', intake.demand_access, name='demand-access'),
    path('atendimentos/<uuid:pk>/etapa/', intake.demand_stage, name='demand-stage'),
    path('atendimentos/<uuid:pk>/encaminhar/', intake.handoff_send, name='handoff-send'),
    path('atendimentos/<uuid:pk>/cancelar-passagem/', intake.handoff_cancel, name='handoff-cancel'),
    path('passagens/', intake.handoffs, name='handoffs'),
    path('passagens/<uuid:pk>/decidir/', intake.handoff_decide, name='handoff-decide'),
    path('gestao/acessos-negocio/', intake.business_access, name='business-access'),
    path('gestao/recuperacao/', intake.recovery, name='recovery'),
    path('gestao/recuperacao/<uuid:pk>/', intake.recover, name='demand-recover'),
    path('', RedirectView.as_view(url='/meu-trabalho/', permanent=False)),
    path('entrar/', identity.InternalLoginView.as_view(), name='login'),
    path('sair/', identity.InternalLogoutView.as_view(), name='logout'),
    path('meu-trabalho/', identity.dashboard, name='dashboard'),
    path('administracao/usuarios/', identity.users, name='users'),
    path('administracao/usuarios/novo/', identity.user_create, name='user-create'),
    path('administracao/usuarios/<int:pk>/', identity.user_edit, name='user-edit'),
    path('administracao/usuarios/<int:pk>/revogar/', identity.user_revoke, name='user-revoke'),
    path('historico/', history, name='history'),
    path('casos/', cases.case_list, name='cases'),
    path('casos/<uuid:pk>/', cases.case_detail, name='case-detail'),
    path('casos/<uuid:pk>/exportar/', cases.case_export, name='case-export'),
]
