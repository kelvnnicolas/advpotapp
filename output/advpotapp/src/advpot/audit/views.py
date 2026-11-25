from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from .models import AuditEvent


@never_cache
@login_required
def history(request):
    if not request.user.can_read_audit:
        raise PermissionDenied
    page = Paginator(AuditEvent.objects.select_related('actor'), 30).get_page(request.GET.get('page'))
    return render(request, 'audit/history.html', {'page_obj': page})
