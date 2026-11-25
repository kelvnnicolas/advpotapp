from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from advpot.audit.services import record


@receiver(user_logged_in)
def session_started(sender, request, user, **kwargs):
    request.session['identity_version'] = user.session_version
    record(actor=user, action='session.login', target=user.pk)


@receiver(user_logged_out)
def session_ended(sender, request, user, **kwargs):
    if user and user.pk:
        record(actor=user, action='session.logout', target=user.pk)
