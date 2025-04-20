import pytest
from django.http import HttpRequest
from django.test import override_settings
from django.contrib.auth import get_user_model

from django_solomon.backends import MagicLinkBackend
from django_solomon.models import MagicLink

User = get_user_model()


@pytest.mark.django_db
class TestMagicLinkBackend:
    """Tests for the MagicLinkBackend class."""

    def setup_method(self):
        """Set up the test environment."""
        self.backend = MagicLinkBackend()
        self.request = HttpRequest()

    def test_authenticate_no_token(self):
        """Test authentication with no token."""
        user = self.backend.authenticate(request=self.request, token=None)
        assert user is None

        user = self.backend.authenticate(request=self.request, token="")
        assert user is None

    def test_authenticate_invalid_token(self):
        """Test authentication with an invalid token."""
        user = self.backend.authenticate(request=self.request, token="invalid-token")
        assert user is None
        assert hasattr(self.request, "magic_link_error")
        # Just check that an error message is set, not its exact content
        assert self.request.magic_link_error

    def test_authenticate_expired_token(self, expired_magic_link):
        """Test authentication with an expired token."""
        user = self.backend.authenticate(request=self.request, token=expired_magic_link.token)
        assert user is None
        assert hasattr(self.request, "magic_link_error")
        # Just check that an error message is set, not its exact content
        assert self.request.magic_link_error

    def test_authenticate_used_token(self, used_magic_link):
        """Test authentication with a used token."""
        user = self.backend.authenticate(request=self.request, token=used_magic_link.token)
        assert user is None
        assert hasattr(self.request, "magic_link_error")
        # Just check that an error message is set, not its exact content
        assert self.request.magic_link_error

    def test_authenticate_valid_token(self, magic_link):
        """Test authentication with a valid token."""
        user = self.backend.authenticate(request=self.request, token=magic_link.token)
        assert user == magic_link.user

        # Verify the magic link was marked as used
        magic_link.refresh_from_db()
        assert magic_link.used

    def test_authenticate_without_request(self, magic_link):
        """Test authentication without a request object."""
        user = self.backend.authenticate(token=magic_link.token)
        assert user == magic_link.user

    @override_settings(SOLOMON_ALLOW_ADMIN_LOGIN=False)
    def test_authenticate_admin_disallowed(self, user):
        """Test authentication for admin users when they are not allowed to login."""
        # Make the user a superuser
        user.is_superuser = True
        user.save()

        # Create a magic link for the admin user
        magic_link = MagicLink.objects.create_for_user(user)

        # Try to authenticate
        authenticated_user = self.backend.authenticate(request=self.request, token=magic_link.token)
        assert authenticated_user is None
        assert hasattr(self.request, "magic_link_error")
        # Just check that an error message is set, not its exact content
        assert self.request.magic_link_error

    @override_settings(SOLOMON_ALLOW_ADMIN_LOGIN=True)
    def test_authenticate_admin_allowed(self, user):
        """Test authentication for admin users when they are allowed to login."""
        # Make the user a superuser
        user.is_superuser = True
        user.save()

        # Create a magic link for the admin user
        magic_link = MagicLink.objects.create_for_user(user)

        # Try to authenticate
        authenticated_user = self.backend.authenticate(request=self.request, token=magic_link.token)
        assert authenticated_user == user

    @override_settings(SOLOMON_ALLOW_STAFF_LOGIN=False)
    def test_authenticate_staff_disallowed(self, user):
        """Test authentication for staff users when they are not allowed to login."""
        # Make the user a staff member but not a superuser
        user.is_staff = True
        user.is_superuser = False
        user.save()

        # Create a magic link for the staff user
        magic_link = MagicLink.objects.create_for_user(user)

        # Try to authenticate
        authenticated_user = self.backend.authenticate(request=self.request, token=magic_link.token)
        assert authenticated_user is None
        assert hasattr(self.request, "magic_link_error")
        # Just check that an error message is set, not its exact content
        assert self.request.magic_link_error

    @override_settings(SOLOMON_ALLOW_STAFF_LOGIN=True)
    def test_authenticate_staff_allowed(self, user):
        """Test authentication for staff users when they are allowed to login."""
        # Make the user a staff member but not a superuser
        user.is_staff = True
        user.is_superuser = False
        user.save()

        # Create a magic link for the staff user
        magic_link = MagicLink.objects.create_for_user(user)

        # Try to authenticate
        authenticated_user = self.backend.authenticate(request=self.request, token=magic_link.token)
        assert authenticated_user == user

    def test_authenticate_no_request_with_error(self, user):
        """Test authentication without a request object when an error occurs."""
        # Make the user a superuser
        user.is_superuser = True
        user.save()

        # Create a magic link for the admin user
        magic_link = MagicLink.objects.create_for_user(user)

        # Try to authenticate with settings that would normally set an error
        with override_settings(SOLOMON_ALLOW_ADMIN_LOGIN=False):
            authenticated_user = self.backend.authenticate(token=magic_link.token)
            assert authenticated_user is None
            # No error should be set since there's no request object

    def test_authenticate_invalid_token_no_request(self):
        """Test authentication with an invalid token and no request object."""
        # This test covers the case where magic_link is None and request is None
        user = self.backend.authenticate(token="invalid-token", request=None)
        assert user is None
        # No error should be set since there's no request object

    @override_settings(SOLOMON_ALLOW_STAFF_LOGIN=False)
    def test_authenticate_staff_disallowed_no_request(self, user):
        """Test authentication for staff users when they are not allowed to login and no request object."""
        # Make the user a staff member but not a superuser
        user.is_staff = True
        user.is_superuser = False
        user.save()

        # Create a magic link for the staff user
        magic_link = MagicLink.objects.create_for_user(user)

        # Try to authenticate without a request object
        authenticated_user = self.backend.authenticate(token=magic_link.token, request=None)
        assert authenticated_user is None
        # No error should be set since there's no request object
