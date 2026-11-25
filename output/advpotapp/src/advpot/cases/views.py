import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from advpot.audit.services import record
from .models import CaseGrant
from .queries import visible_cases


@never_cache
@login_required
def case_list(request):
    query = request.GET.get('q', '').strip()[:180]
    queryset = visible_cases(request.user)
    if query:
        queryset = queryset.filter(title__icontains=query)
    page = Paginator(queryset, 20).get_page(request.GET.get('page'))
    return render(request, 'cases/list.html', {'page_obj': page, 'q': query})


@never_cache
@login_required
def case_detail(request, pk):
    case = get_object_or_404(visible_cases(request.user), pk=pk)
    return render(request, 'cases/detail.html', {
        'case': case,
        'can_export': visible_cases(request.user, action=CaseGrant.Action.EXPORT).filter(pk=pk).exists(),
    })


@never_cache
@login_required
@require_POST
def case_export(request, pk):
    case = get_object_or_404(visible_cases(request.user, action=CaseGrant.Action.EXPORT), pk=pk)
    record(actor=request.user, action='case.export', target=case.pk)
    response = HttpResponse(json.dumps({'schema': 'advpot.case-envelope.v1', 'case': {
        'id': str(case.pk), 'title': case.title, 'responsible_user_id': case.responsible_id,
        'created_at': case.created_at.isoformat(),
    }}, ensure_ascii=False, indent=2), content_type='application/json; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="caso-{case.pk}.json"'
    return response
