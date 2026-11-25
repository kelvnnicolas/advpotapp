from .models import Case, CaseGrant


def visible_cases(user, *, action=CaseGrant.Action.VIEW):
    if not user.is_authenticated or not user.is_active:
        return Case.objects.none()
    queryset = Case.objects.filter(grants__user=user, grants__action=CaseGrant.Action.VIEW)
    if action != CaseGrant.Action.VIEW:
        queryset = queryset.filter(grants__user=user, grants__action=action)
    return queryset.distinct()
