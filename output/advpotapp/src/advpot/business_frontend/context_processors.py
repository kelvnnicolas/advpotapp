from django.conf import settings


def preview_navigation(request):
    return {'business_preview_enabled': settings.DEBUG}
