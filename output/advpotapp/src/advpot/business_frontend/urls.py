from django.urls import path
from . import views

app_name = 'business'
urlpatterns = [
    path('business/', views.private_page, {'page_name': 'index'}, name='index'),
    path('business/equipe/', views.private_page, {'page_name': 'team'}, name='team'),
    path('business/fluxos/', views.private_page, {'page_name': 'flows'}, name='flows'),
    path('business/assinatura/', views.private_page, {'page_name': 'subscription'}, name='subscription'),
    path('business/integracoes/', views.private_page, {'page_name': 'integrations'}, name='integrations'),
    path('business/configuracoes/', views.private_page, {'page_name': 'settings'}, name='settings'),
    path('contratar/', views.public_page, {'page_name': 'contract'}, name='contract'),
    path('contratar/retorno/', views.public_page, {'page_name': 'return'}, name='return'),
]
