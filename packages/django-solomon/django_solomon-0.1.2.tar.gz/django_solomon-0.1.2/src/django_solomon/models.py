from datetime import timedelta
from typing import Any, TypeVar

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()
UserType = TypeVar("UserType", bound=AbstractBaseUser)


class BlacklistedEmail(models.Model):
    """
    Model to store blacklisted email addresses.

    These emails will be blocked from using the magic login feature.
    """

    email = models.EmailField(_("Email"), max_length=255, unique=True)
    reason = models.TextField(_("Reason"), blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Blacklisted Email")
        verbose_name_plural = _("Blacklisted Emails")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.email


class MagicLinkManager(models.Manager["MagicLink"]):
    """
    Manages the creation and retrieval of MagicLink instances.

    This manager provides utility methods to handle magic links, such as creating a
    new magic link for a user and retrieving valid magic links based on specific
    criteria like token, usage status, and expiration date.
    """

    def create_for_user(self, user: UserType) -> "MagicLink":
        """
        Creates a new magic link for a given user. If the setting SOLOMON_ONLY_ONE_LINK_ALLOWED
        is enabled, marks existing links for the user as used before creating a new one.

        Args:
            user (UserType): The user for whom the magic link should be created.

        Returns:
            MagicLink: The newly created magic link instance.
        """
        if getattr(settings, "SOLOMON_ONLY_ONE_LINK_ALLOWED", True):
            self.filter(user=user).update(used=True)
        return self.create(user=user)

    def get_valid_link(self, token: str) -> "MagicLink":
        """
        Returns the first valid magic link that matches the given token.

        A valid magic link is identified by a unique token, marked as unused, and
        has an expiration date greater than or equal to the current time. The
        method searches for a link meeting these conditions and returns the first
        result if found.

        Args:
            token (str): The unique token used to identify the magic link.

        Returns:
            MagicLink: An instance of the valid MagicLink, or None if no valid link
            is found.
        """
        return self.filter(token=token, used=False, expires_at__gte=timezone.now()).first()


class MagicLink(models.Model):
    """
    Model to store magic links for authentication.

    This model supports both the standard User model and custom User models.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="magic_links", verbose_name=_("User")
    )
    token = models.CharField(_("Token"), max_length=100, unique=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    expires_at = models.DateTimeField(_("Expires at"))
    used = models.BooleanField(_("Used"), default=False)

    objects = MagicLinkManager()

    class Meta:
        verbose_name = _("Magic Link")
        verbose_name_plural = _("Magic Links")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Magic Link for {self.user}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Saves the instance of the object, ensuring that a token and expiration
        time are generated and set if not already provided. The token is created
        using a default token generator, and the expiration time is calculated
        based on a predefined duration from the settings.
        """
        if not self.pk or not self.token:
            self.token = default_token_generator.make_token(self.user)

        if not self.expires_at:
            expiration_time = getattr(settings, "SOLOMON_LINK_EXPIRATION", 300)  # seconds
            self.expires_at = timezone.now() + timedelta(seconds=expiration_time)

        super().save(*args, **kwargs)

    @property
    def is_expired(self) -> bool:
        """Check if the magic link has expired."""
        return self.expires_at < timezone.now()

    @property
    def is_valid(self) -> bool:
        """Check if the magic link is valid (not used and not expired)."""
        return not self.used and not self.is_expired

    def use(self) -> None:
        """Mark the magic link as used."""
        self.used = True
        self.save(update_fields=["used"])
