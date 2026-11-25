from django.contrib.auth import logout
from django.conf import settings
from django.http import HttpResponse


class SessionVersionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            version = request.session.get('identity_version')
            if version != request.user.session_version:
                logout(request)
        response = self.get_response(request)
        if (request.headers.get('HX-Request') == 'true' and response.status_code == 302
                and response.headers.get('Location', '').startswith(settings.LOGIN_URL)):
            response = HttpResponse(status=200, headers={'HX-Redirect': response.headers['Location']})
        if not request.path.startswith(settings.STATIC_URL):
            response['Cache-Control'] = 'no-store, private, max-age=0'
        return response
