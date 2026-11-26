from .access import departments, is_authority


def navigation(request):
    memberships = departments(request.user)
    authority = is_authority(request.user)
    return {'nav_intake': bool(memberships), 'nav_business_access': authority, 'nav_recovery': authority or 'management' in memberships}
