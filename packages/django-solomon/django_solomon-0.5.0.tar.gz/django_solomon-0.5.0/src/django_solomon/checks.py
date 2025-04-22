# django_solomon/checks.py
from django.apps import apps
from django.conf import settings
from django.core.checks import Error, register


@register()
def check_user_model_email(app_configs, **kwargs):  # noqa: ARG001
    """
    Check that the user model has a unique email field.
    """
    errors = []

    # Get the user model
    user_model = apps.get_model(settings.AUTH_USER_MODEL)

    # Check if email field exists
    try:
        email_field = user_model._meta.get_field("email")
    except Exception:
        errors.append(
            Error(
                "User model does not have an email field.",
                hint="Make sure your user model has an email field.",
                obj=settings.AUTH_USER_MODEL,
                id="django_solomon.E001",
            )
        )
        return errors

    # Check if email field is unique
    if not email_field.unique:
        errors.append(
            Error(
                "User model email field must be unique.",
                hint="Set unique=True on the email field of your user model.",
                obj=settings.AUTH_USER_MODEL,
                id="django_solomon.E002",
            )
        )

    return errors
