import os
os.environ.setdefault('ADVPOT_SECRET_KEY', 'tests-only-not-a-deployment-secret')
os.environ['ADVPOT_ENV'] = 'local'
from .settings import *  # noqa: F403

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']
