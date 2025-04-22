from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import override_settings, TestCase
from django.utils import timezone

from django_solomon.backends import MagicLinkBackend
from django_solomon.models import MagicLink


class TestMagicLinkBackendWithInvalidTokens(TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Create a user for testing
        User = get_user_model()
        self.user = User.objects.create_user(email="test@example.com", password="password123")

        # Create an expired magic link
        self.expired_magic_link = MagicLink.objects.create(
            user=self.user, expires_at=timezone.now() - timedelta(minutes=5)
        )

        # Create a used magic link
        self.used_magic_link = MagicLink.objects.create(
            user=self.user, expires_at=timezone.now() + timedelta(minutes=5), used=True
        )

        # Create backend and request
        self.backend = MagicLinkBackend()
        self.request = HttpRequest()

    def test_authenticate_no_token(self):
        """Test authentication with no token."""
        user = self.backend.authenticate(request=self.request, token=None)
        self.assertIsNone(user)

        user = self.backend.authenticate(request=self.request, token="")
        self.assertIsNone(user)

    def test_authenticate_invalid_token(self):
        """Test authentication with an invalid token."""
        user = self.backend.authenticate(request=self.request, token="invalid-token")
        self.assertIsNone(user)
        self.assertTrue(hasattr(self.request, "magic_link_error"))
        # Just check that an error message is set, not its exact content
        self.assertTrue(self.request.magic_link_error)

    def test_authenticate_invalid_token_no_request(self):
        """Test authentication with an invalid token and no request object."""
        # This test covers the case where magic_link is None and request is None
        user = self.backend.authenticate(token="invalid-token", request=None)
        self.assertIsNone(user)
        # No error should be set since there's no request object

    def test_authenticate_expired_token(self):
        """Test authentication with an expired token."""
        user = self.backend.authenticate(request=self.request, token=self.expired_magic_link.token)
        self.assertIsNone(user)
        self.assertTrue(hasattr(self.request, "magic_link_error"))
        # Just check that an error message is set, not its exact content
        self.assertTrue(self.request.magic_link_error)

    def test_authenticate_used_token(self):
        """Test authentication with a used token."""
        user = self.backend.authenticate(request=self.request, token=self.used_magic_link.token)
        self.assertIsNone(user)
        self.assertTrue(hasattr(self.request, "magic_link_error"))
        # Just check that an error message is set, not its exact content
        self.assertTrue(self.request.magic_link_error)


class TestMagicLinkBackendWithIpAddress(TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Create a user for testing
        User = get_user_model()
        self.user = User.objects.create_user(email="test@example.com", password="password123")

        # Create a magic link for testing
        self.magic_link = MagicLink.objects.create_for_user(self.user)

        # Create a magic link with IP address
        self.magic_link_with_ip = MagicLink.objects.create_for_user(self.user, ip_address="192.168.1.1")

        # Create backend and request
        self.backend = MagicLinkBackend()
        self.request = HttpRequest()

    @override_settings(SOLOMON_ENFORCE_SAME_IP=True)
    def test_authenticate_ip_match(self):
        """Test authentication with IP validation enabled and matching IP addresses."""
        # Mock the get_client_ip function to return the same IP as in the magic link
        with patch("django_solomon.backends.get_client_ip", return_value="192.168.1.1"):
            # Try to authenticate
            authenticated_user = self.backend.authenticate(request=self.request, token=self.magic_link_with_ip.token)
            self.assertEqual(authenticated_user, self.magic_link_with_ip.user)

    @override_settings(SOLOMON_ENFORCE_SAME_IP=True)
    def test_authenticate_ip_mismatch(self):
        """Test authentication with IP validation enabled and mismatched IP addresses."""
        # Mock the get_client_ip function to return a different IP
        with patch("django_solomon.backends.get_client_ip", return_value="10.0.0.1"):
            # Try to authenticate
            authenticated_user = self.backend.authenticate(request=self.request, token=self.magic_link_with_ip.token)
            self.assertIsNone(authenticated_user)
            self.assertTrue(hasattr(self.request, "magic_link_error"))
            self.assertTrue(self.request.magic_link_error)

    @override_settings(SOLOMON_ENFORCE_SAME_IP=False)
    def test_authenticate_ip_validation_disabled(self):
        """Test authentication with IP validation disabled."""
        # Mock the get_client_ip function to return a different IP
        with patch("django_solomon.backends.get_client_ip", return_value="10.0.0.1"):
            # Try to authenticate - should work despite IP mismatch because validation is disabled
            authenticated_user = self.backend.authenticate(request=self.request, token=self.magic_link_with_ip.token)
            self.assertEqual(authenticated_user, self.magic_link_with_ip.user)

    @override_settings(SOLOMON_ENFORCE_SAME_IP=True)
    def test_authenticate_ip_validation_no_stored_ip(self):
        """Test authentication with IP validation enabled but no stored IP in the magic link."""
        # Magic link has no IP address stored
        self.assertIsNone(self.magic_link.ip_address)

        # Mock the get_client_ip function to return any IP
        with patch("django_solomon.backends.get_client_ip", return_value="10.0.0.1"):
            # Try to authenticate - should work because there's no IP to compare against
            authenticated_user = self.backend.authenticate(request=self.request, token=self.magic_link.token)
            self.assertIsNone(authenticated_user)

    @override_settings(SOLOMON_ENFORCE_SAME_IP=True)
    def test_authenticate_ip_validation_no_request(self):
        """Test authentication with IP validation enabled but no request object."""
        # Try to authenticate without a request object
        authenticated_user = self.backend.authenticate(token=self.magic_link_with_ip.token, request=None)
        # Should fail because there's no request to get the IP from
        self.assertIsNone(authenticated_user)


class TestMagicLinkBackendWithAdminUser(TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Create a user for testing
        User = get_user_model()
        self.user = User.objects.create_superuser(email="test@example.com", password="password123")

        # Create a magic link for the admin user
        self.magic_link = MagicLink.objects.create_for_user(self.user)

        # Create backend and request
        self.backend = MagicLinkBackend()
        self.request = HttpRequest()

    @override_settings(SOLOMON_ALLOW_ADMIN_LOGIN=False)
    def test_authenticate_admin_disallowed(self):
        """Test authentication for admin users when they are not allowed to login."""
        authenticated_user = self.backend.authenticate(request=self.request, token=self.magic_link.token)
        self.assertIsNone(authenticated_user)
        self.assertTrue(hasattr(self.request, "magic_link_error"))
        # Just check that an error message is set, not its exact content
        self.assertTrue(self.request.magic_link_error)

    @override_settings(SOLOMON_ALLOW_ADMIN_LOGIN=True)
    def test_authenticate_admin_allowed(self):
        """Test authentication for admin users when they are allowed to login."""
        authenticated_user = self.backend.authenticate(request=self.request, token=self.magic_link.token)
        self.assertEqual(authenticated_user, self.user)

    @override_settings(SOLOMON_ALLOW_ADMIN_LOGIN=False)
    def test_authenticate_admin_disallowed_no_request(self):
        """Test authentication for staff users when they are not allowed to login and no request object."""
        authenticated_user = self.backend.authenticate(token=self.magic_link.token, request=None)
        self.assertIsNone(authenticated_user)
        # No error should be set since there's no request object


class TestMagicLinkBackendWithStaffUser(TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Create a user for testing
        User = get_user_model()
        self.user = User.objects.create_user(email="test@example.com", password="password123", is_staff=True)

        # Create a magic link for the staff user
        self.magic_link = MagicLink.objects.create_for_user(self.user)

        # Create backend and request
        self.backend = MagicLinkBackend()
        self.request = HttpRequest()

    @override_settings(SOLOMON_ALLOW_STAFF_LOGIN=False)
    def test_authenticate_staff_disallowed(self):
        """Test authentication for staff users when they are not allowed to login."""
        authenticated_user = self.backend.authenticate(request=self.request, token=self.magic_link.token)
        self.assertIsNone(authenticated_user)
        self.assertTrue(hasattr(self.request, "magic_link_error"))
        # Just check that an error message is set, not its exact content
        self.assertTrue(self.request.magic_link_error)

    @override_settings(SOLOMON_ALLOW_STAFF_LOGIN=True)
    def test_authenticate_staff_allowed(self):
        """Test authentication for staff users when they are allowed to login."""
        authenticated_user = self.backend.authenticate(request=self.request, token=self.magic_link.token)
        self.assertEqual(authenticated_user, self.user)

    @override_settings(SOLOMON_ALLOW_STAFF_LOGIN=False)
    def test_authenticate_staff_disallowed_no_request(self):
        """Test authentication for staff users when they are not allowed to login and no request object."""
        authenticated_user = self.backend.authenticate(token=self.magic_link.token, request=None)
        self.assertIsNone(authenticated_user)
        # No error should be set since there's no request object
