from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from django_solomon.models import BlacklistedEmail, MagicLink


@admin.register(BlacklistedEmail)
class BlacklistedEmailAdmin(admin.ModelAdmin):
    """Admin interface for BlacklistedEmail model."""

    list_display = ("email", "reason", "created_at")
    list_filter = ("created_at",)
    search_fields = ("email", "reason")
    date_hierarchy = "created_at"

    fieldsets = (
        (None, {"fields": ("email", "reason")}),
        (_("Dates"), {"fields": ("created_at",)}),
    )
    readonly_fields = ("created_at",)


@admin.register(MagicLink)
class MagicLinkAdmin(admin.ModelAdmin):
    """Admin interface for MagicLink model."""

    list_display = ("user", "created_at", "expires_at", "used", "is_valid")
    list_filter = ("used", "created_at", "expires_at")
    search_fields = ("user__username", "user__email", "token")
    readonly_fields = ("id", "token", "created_at", "is_valid")
    date_hierarchy = "created_at"

    fieldsets = (
        (None, {"fields": ("id", "user", "token")}),
        (_("Status"), {"fields": ("used", "is_valid")}),
        (_("Dates"), {"fields": ("created_at", "expires_at")}),
    )

    @admin.display(
        description=_("Valid"),
        boolean=True,
    )
    def is_valid(self, obj: MagicLink) -> bool:
        """Display if the magic link is valid."""
        return obj.is_valid
