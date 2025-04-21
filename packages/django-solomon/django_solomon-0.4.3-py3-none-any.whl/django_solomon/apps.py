from django.apps import AppConfig


class DjangoSolomonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_solomon"

    def ready(self):
        # Copyright (c) 2023 Carlton Gibson
        # This migration is taken from the fantastic project `django-unique-user-email` created by Carlton Gibson.
        # https://github.com/carltongibson/django-unique-user-email/

        from django.contrib.auth.models import User
        from django.db import models

        # Updating the field itself triggers the auto-detector
        # field = User._meta.get_field("email")
        # field._unique = True
        #
        # But setting a constraint does not...
        User.Meta.constraints = [
            models.UniqueConstraint(
                fields=["email"],
                name="unique_user_email",
                # deferrable=models.Deferrable.DEFERRED,
            ),
        ]
        User._meta.constraints = User.Meta.constraints
        # ... as long as original_attrs is not updated.
        # User._meta.original_attrs["constraints"] = User.Meta.constraints
