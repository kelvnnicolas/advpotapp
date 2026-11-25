from django.urls import path
from django.views.generic import RedirectView
from advpot.identity import views as identity
from advpot.cases import views as cases
from advpot.audit.views import history

urlpatterns = [
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
