from django.apps import AppConfig


class DjangoSolomonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_solomon"

    def ready(self):
        # Import checks when app is ready
        import django_solomon.checks  # noqa
