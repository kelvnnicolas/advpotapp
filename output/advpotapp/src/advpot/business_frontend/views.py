from functools import wraps
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_safe
from .contracts import SCENARIOS, get_preview

PAGES = {
    'index': 'Visão do escritório', 'team': 'Equipe', 'flows': 'Fluxos',
    'subscription': 'Assinatura', 'integrations': 'Integrações', 'settings': 'Configurações',
    'contract': 'Contratar Business', 'return': 'Retorno da contratação',
}


def local_preview(view):
    @wraps(view)
    def guarded(request, *args, **kwargs):
        if not settings.DEBUG:
            raise Http404
        return view(request, *args, **kwargs)
    return guarded


def page(request, page_name):
    scenario = request.GET.get('scenario', 'active')
    try:
        preview = get_preview(scenario)
    except ValueError:
        raise Http404 from None
    return render(request, f'business/{page_name}.html', {
        'preview': preview, 'scenario': scenario, 'scenarios': SCENARIOS,
        'page_name': page_name, 'page_title': PAGES[page_name],
        'business_pages': [{'key': key, 'label': label, 'url': f'business:{key}'} for key, label in PAGES.items() if key not in {'contract', 'return'}],
    })


@local_preview
@login_required
@require_safe
def private_page(request, page_name):
    return page(request, page_name)


@local_preview
@require_safe
def public_page(request, page_name):
    return page(request, page_name)
