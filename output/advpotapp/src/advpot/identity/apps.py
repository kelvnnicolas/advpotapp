from django.apps import AppConfig


class IdentityConfig(AppConfig):
    name = 'advpot.identity'

    def ready(self):
        from . import signals  # noqa: F401
