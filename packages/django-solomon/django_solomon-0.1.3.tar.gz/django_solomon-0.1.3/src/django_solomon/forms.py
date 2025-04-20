from django import forms
from django.utils.translation import gettext_lazy as _


class MagicLinkForm(forms.Form):
    """Form for requesting a magic link."""

    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )
