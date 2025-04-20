from typing import Any

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from django_solomon.models import MagicLink, UserType


class MagicLinkBackend(ModelBackend):
    def authenticate(
        self,
        request: HttpRequest | None = None,
        token: str | None = None,
        **kwargs: Any,  # noqa: ARG002
    ) -> UserType | None:
        """
        Authenticates a user based on the provided magic link token. This method validates
        the token, ensures the token is not expired, and checks if the user associated
        with the token is allowed to login based on their role and the application's
        settings.

        Args:
            request (HttpRequest | None): The HTTP request object. Defaults to None.
                It is used to store error messages in case the authentication fails.
            token (str | None): A unique string token from the magic link used for
                authentication. If None, authentication cannot proceed.

        Returns:
            Any: Returns the authenticated user object if the token is valid and
                the user is allowed to log in. Returns None if the token is invalid,
                expired, or if the user is not permitted to log in.
        """
        if not token:
            return None

        magic_link = MagicLink.objects.get_valid_link(token)
        if not magic_link:
            if request:
                request.magic_link_error = _("Invalid or expired magic link")
            return None

        # Mark the magic link as used
        magic_link.use()

        user = magic_link.user

        # Check if user is admin and if they are allowed to login
        if user.is_superuser and not getattr(settings, "SOLOMON_ALLOW_ADMIN_LOGIN", True):
            if request:
                request.magic_link_error = _("Admin users are not allowed to login via magic links")
            return None

        # Check if user is staff (but not admin) and if they are allowed to login
        if user.is_staff and not user.is_superuser and not getattr(settings, "SOLOMON_ALLOW_STAFF_LOGIN", True):
            if request:
                request.magic_link_error = _("Staff users are not allowed to login via magic links")
            return None

        return user
