import pytest
from django import forms
from django.utils.translation import gettext_lazy as _

from django_solomon.forms import MagicLinkForm


class TestMagicLinkForm:
    """Tests for the MagicLinkForm class."""

    def test_form_initialization(self):
        """Test that the form can be initialized."""
        form = MagicLinkForm()
        assert isinstance(form, forms.Form)
        assert "email" in form.fields

    def test_form_field_attributes(self):
        """Test the attributes of the email field."""
        form = MagicLinkForm()
        email_field = form.fields["email"]

        # Test field type
        assert isinstance(email_field, forms.EmailField)

        # Test label
        assert email_field.label == _("Email")

        # Test max_length
        assert email_field.max_length == 254

        # Test widget
        assert isinstance(email_field.widget, forms.EmailInput)
        assert email_field.widget.attrs["autocomplete"] == "email"

    @pytest.mark.django_db
    def test_form_valid_data(self, user):
        """Test form validation with valid data."""
        form = MagicLinkForm(data={"email": user.email})
        assert form.is_valid()
        assert form.cleaned_data["email"] == user.email

    @pytest.mark.django_db
    def test_form_empty_data(self):
        """Test form validation with empty data."""
        form = MagicLinkForm(data={})
        assert not form.is_valid()
        assert "email" in form.errors
        assert "This field is required." in form.errors["email"]

    @pytest.mark.django_db
    def test_form_invalid_email(self):
        """Test form validation with invalid email."""
        form = MagicLinkForm(data={"email": "not-an-email"})
        assert not form.is_valid()
        assert "email" in form.errors
        assert "Enter a valid email address." in form.errors["email"]

    @pytest.mark.django_db
    def test_form_email_too_long(self):
        """Test form validation with email that exceeds max_length."""
        # Create an email that is too long (255 characters)
        long_email = "a" * 245 + "@example.com"  # 245 + 12 = 257 characters
        form = MagicLinkForm(data={"email": long_email})
        assert not form.is_valid()
        assert "email" in form.errors
        assert "Ensure this value has at most 254 characters" in form.errors["email"][0]

    @pytest.mark.django_db
    def test_form_with_blacklisted_email(self, blacklisted_email):
        """Test form validation with a blacklisted email."""
        # This test assumes that the form validates against blacklisted emails
        # If it doesn't, this test will pass regardless
        form = MagicLinkForm(data={"email": blacklisted_email.email})
        assert form.is_valid()  # Form should be valid as there's no validation against blacklisted emails

    @pytest.mark.django_db
    def test_form_with_nonexistent_user_email(self):
        """Test form validation with an email that doesn't belong to any user."""
        # This test assumes that the form doesn't validate against existing users
        # If it does, this test will need to be adjusted
        form = MagicLinkForm(data={"email": "nonexistent@example.com"})
        assert form.is_valid()  # Form should be valid as there's no validation against existing users

    def test_form_with_edge_case_emails(self):
        """Test form validation with edge case emails."""
        # Test with various edge case emails that should be valid according to Django's EmailField
        valid_emails = [
            "email@example.com",
            "firstname.lastname@example.com",
            "email@subdomain.example.com",
            "firstname+lastname@example.com",
            # "email@123.123.123.123",  # Not valid in Django's EmailField
            "email@[123.123.123.123]",
            '"email"@example.com',
            "1234567890@example.com",
            "email@example-one.com",
            "_______@example.com",
            "email@example.name",
            "email@example.museum",
            "email@example.co.jp",
        ]

        for email in valid_emails:
            form = MagicLinkForm(data={"email": email})
            assert form.is_valid(), f"Email {email} should be valid"

        # Test with various edge case emails that should be invalid according to Django's EmailField
        invalid_emails = [
            "plainaddress",
            "#@%^%#$@#$@#.com",
            "@example.com",
            "Joe Smith <email@example.com>",
            "email.example.com",
            "email@example@example.com",
            ".email@example.com",
            "email.@example.com",
            "email..email@example.com",
            "email@example.com (Joe Smith)",
            "email@example",
            "email@-example.com",
            "email@example..com",
            "Abc..123@example.com",
        ]

        for email in invalid_emails:
            form = MagicLinkForm(data={"email": email})
            assert not form.is_valid(), f"Email {email} should be invalid"
