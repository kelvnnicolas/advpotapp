from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from django.utils.crypto import salted_hmac
from .models import LoginBucket

WINDOW = timedelta(minutes=15)


def reserve_attempt(request, username):
    """Reserve before authentication, under row locks shared across web workers."""
    # Lock the IP first so a blocked source cannot allocate more account rows.
    keys = [
        (salted_hmac('login-ip', request.META.get('REMOTE_ADDR', ''), algorithm='sha256').hexdigest(), 20),
        (salted_hmac('login-name', username.strip().casefold(), algorithm='sha256').hexdigest(), 5),
    ]
    now = timezone.now()
    with transaction.atomic():
        for key, limit in keys:
            LoginBucket.objects.get_or_create(key=key)
            bucket = LoginBucket.objects.select_for_update().get(key=key)
            if now - bucket.started_at >= WINDOW:
                bucket.started_at, bucket.attempts = now, 0
            if bucket.attempts >= limit:
                return False
            bucket.attempts += 1
            bucket.save(update_fields=['attempts', 'started_at'])
    return True


def clear_account_attempts(username):
    key = salted_hmac('login-name', username.strip().casefold(), algorithm='sha256').hexdigest()
    LoginBucket.objects.filter(key=key).update(attempts=0)
