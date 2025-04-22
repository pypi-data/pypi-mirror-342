from django import forms
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from django_solomon.forms import MagicLinkForm, CustomUserCreationForm, CustomUserChangeForm
from django_solomon.models import BlacklistedEmail, CustomUser


class TestMagicLinkForm(TestCase):
    """Tests for the MagicLinkForm class."""

    def setUp(self):
        """Set up test environment."""
        # Create a user for testing
        from django.contrib.auth import get_user_model

        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")

        # Create a blacklisted email for testing
        self.blacklisted_email = BlacklistedEmail.objects.create(
            email="blacklisted@example.com", reason="Testing purposes"
        )

    def test_form_initialization(self):
        """Test that the form can be initialized."""
        form = MagicLinkForm()
        self.assertIsInstance(form, forms.Form)
        self.assertIn("email", form.fields)

    def test_form_field_attributes(self):
        """Test the attributes of the email field."""
        form = MagicLinkForm()
        email_field = form.fields["email"]

        # Test field type
        self.assertIsInstance(email_field, forms.EmailField)

        # Test label
        self.assertEqual(email_field.label, _("Email"))

        # Test max_length
        self.assertEqual(email_field.max_length, 254)

        # Test widget
        self.assertIsInstance(email_field.widget, forms.EmailInput)
        self.assertEqual(email_field.widget.attrs["autocomplete"], "email")

    def test_form_valid_data(self):
        """Test form validation with valid data."""
        form = MagicLinkForm(data={"email": self.user.email})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["email"], self.user.email)

    def test_form_empty_data(self):
        """Test form validation with empty data."""
        form = MagicLinkForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("This field is required.", form.errors["email"])

    def test_form_invalid_email(self):
        """Test form validation with invalid email."""
        form = MagicLinkForm(data={"email": "not-an-email"})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("Enter a valid email address.", form.errors["email"])

    def test_form_email_too_long(self):
        """Test form validation with email that exceeds max_length."""
        # Create an email that is too long (255 characters)
        long_email = "a" * 245 + "@example.com"  # 245 + 12 = 257 characters
        form = MagicLinkForm(data={"email": long_email})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("Ensure this value has at most 254 characters", form.errors["email"][0])

    def test_form_with_blacklisted_email(self):
        """Test form validation with a blacklisted email."""
        # This test assumes that the form validates against blacklisted emails
        # If it doesn't, this test will pass regardless
        form = MagicLinkForm(data={"email": self.blacklisted_email.email})
        self.assertTrue(form.is_valid())  # Form should be valid as there's no validation against blacklisted emails

    def test_form_with_nonexistent_user_email(self):
        """Test form validation with an email that doesn't belong to any user."""
        # This test assumes that the form doesn't validate against existing users
        # If it does, this test will need to be adjusted
        form = MagicLinkForm(data={"email": "nonexistent@example.com"})
        self.assertTrue(form.is_valid())  # Form should be valid as there's no validation against existing users

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
            self.assertTrue(form.is_valid(), f"Email {email} should be valid")

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
            self.assertFalse(form.is_valid(), f"Email {email} should be invalid")


class TestCustomUserCreationForm(TestCase):
    """Tests for the CustomUserCreationForm class."""

    def setUp(self):
        """Set up test environment."""
        self.valid_data = {
            "email": "newuser@example.com",
            "password1": "securepassword123",
            "password2": "securepassword123",
        }

    def test_form_initialization(self):
        """Test that the form can be initialized."""
        form = CustomUserCreationForm()
        self.assertTrue("email" in form.fields)
        self.assertTrue("password1" in form.fields)
        self.assertTrue("password2" in form.fields)

    def test_form_valid_data(self):
        """Test form validation with valid data."""
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, self.valid_data["email"])
        self.assertTrue(user.check_password(self.valid_data["password1"]))

    def test_form_passwords_dont_match(self):
        """Test form validation when passwords don't match."""
        data = self.valid_data.copy()
        data["password2"] = "differentpassword"
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_email_already_exists(self):
        """Test form validation when email already exists."""
        # Create a user with the same email
        CustomUser.objects.create_user(email=self.valid_data["email"], password="existingpassword")

        # Try to create another user with the same email
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_meta_attributes(self):
        """Test that the Meta attributes are set correctly."""
        form = CustomUserCreationForm()
        self.assertEqual(form.Meta.model, CustomUser)
        self.assertEqual(form.Meta.fields, ("email",))


class TestCustomUserChangeForm(TestCase):
    """Tests for the CustomUserChangeForm class."""

    def setUp(self):
        """Set up test environment."""
        self.user = CustomUser.objects.create_user(email="existinguser@example.com", password="password123")
        self.valid_data = {
            "email": "updated@example.com",
        }

    def test_form_initialization(self):
        """Test that the form can be initialized."""
        form = CustomUserChangeForm(instance=self.user)
        self.assertTrue("email" in form.fields)
        self.assertEqual(form.initial["email"], self.user.email)

    def test_form_valid_data(self):
        """Test form validation with valid data."""
        form = CustomUserChangeForm(data=self.valid_data, instance=self.user)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, self.valid_data["email"])

    def test_form_email_already_exists(self):
        """Test form validation when email already exists."""
        # Create another user with a different email
        other_user = CustomUser.objects.create_user(email="otheruser@example.com", password="password123")

        # Try to update the first user to have the same email as the second user
        form = CustomUserChangeForm(data={"email": other_user.email}, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_meta_attributes(self):
        """Test that the Meta attributes are set correctly."""
        form = CustomUserChangeForm()
        self.assertEqual(form.Meta.model, CustomUser)
        self.assertEqual(form.Meta.fields, ("email",))
