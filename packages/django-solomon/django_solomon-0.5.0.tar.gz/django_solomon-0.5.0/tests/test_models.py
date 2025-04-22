from datetime import timedelta
from unittest.mock import patch

from django.db import IntegrityError
from django.test import override_settings, TestCase
from django.utils import timezone

from django_solomon.models import BlacklistedEmail, MagicLink


class TestBlacklistedEmail(TestCase):
    """Tests for the BlacklistedEmail model."""

    def setUp(self):
        """Set up test environment."""
        # Create a blacklisted email for testing
        self.blacklisted_email = BlacklistedEmail.objects.create(
            email="blacklisted@example.com", reason="Testing purposes"
        )

    def test_create_blacklisted_email(self):
        """Test creating a blacklisted email."""
        self.assertEqual(self.blacklisted_email.email, "blacklisted@example.com")
        self.assertEqual(self.blacklisted_email.reason, "Testing purposes")
        self.assertIsNotNone(self.blacklisted_email.created_at)

    def test_str_method(self):
        """Test the __str__ method."""
        self.assertEqual(str(self.blacklisted_email), "blacklisted@example.com")

    def test_unique_constraint(self):
        """Test that email must be unique."""
        with self.assertRaises(IntegrityError):
            BlacklistedEmail.objects.create(email="blacklisted@example.com", reason="Another reason")

    def test_create_without_reason(self):
        """Test creating a blacklisted email without a reason."""
        email = BlacklistedEmail.objects.create(email="no-reason@example.com")
        self.assertEqual(email.email, "no-reason@example.com")
        self.assertEqual(email.reason, "")


class TestMagicLinkManager(TestCase):
    """Tests for the MagicLinkManager."""

    def setUp(self):
        """Set up test environment."""
        # Create a user for testing
        from django.contrib.auth import get_user_model

        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")

    def test_create_for_user_default_behavior(self):
        """Test creating a magic link for a user with default settings."""
        # Mock the token generator to return different tokens
        token_count = 0

        def mock_make_token(user):
            nonlocal token_count
            token_count += 1
            return f"token-{token_count}"

        with patch("django.contrib.auth.tokens.default_token_generator.make_token", side_effect=mock_make_token):
            # Create an initial link
            first_link = MagicLink.objects.create_for_user(self.user)
            self.assertEqual(first_link.user, self.user)
            self.assertFalse(first_link.used)
            self.assertIn("token-1", first_link.token)
            self.assertGreater(first_link.expires_at, timezone.now())

            # Create a second link - the first one should be marked as used
            second_link = MagicLink.objects.create_for_user(self.user)
            first_link.refresh_from_db()
            self.assertTrue(first_link.used)
            self.assertFalse(second_link.used)
            self.assertIn("token-2", second_link.token)

    @override_settings(SOLOMON_ONLY_ONE_LINK_ALLOWED=False)
    def test_create_for_user_multiple_links_allowed(self):
        """Test creating multiple magic links for a user when allowed by settings."""
        # Mock the token generator to return different tokens
        token_count = 0

        def mock_make_token(user):
            nonlocal token_count
            token_count += 1
            return f"token-multiple-{token_count}"

        with patch("django.contrib.auth.tokens.default_token_generator.make_token", side_effect=mock_make_token):
            # Create an initial link
            first_link = MagicLink.objects.create_for_user(self.user)
            self.assertIn("token-multiple-1", first_link.token)

            # Create a second link - the first one should NOT be marked as used
            second_link = MagicLink.objects.create_for_user(self.user)
            self.assertIn("token-multiple-2", second_link.token)

            first_link.refresh_from_db()

            self.assertFalse(first_link.used)
            self.assertFalse(second_link.used)
            self.assertEqual(MagicLink.objects.filter(user=self.user, used=False).count(), 2)

    def test_get_valid_link_with_valid_link(self):
        """Test retrieving a valid magic link."""
        # Create a valid magic link
        magic_link = MagicLink.objects.create(user=self.user)
        MagicLink.objects.filter(pk=magic_link.pk).update(token="test-token")
        magic_link.refresh_from_db()

        retrieved_link = MagicLink.objects.get_valid_link(magic_link.token)
        self.assertEqual(retrieved_link, magic_link)

    def test_get_valid_link_with_expired_link(self):
        """Test retrieving an expired magic link returns None."""
        # Create an expired magic link
        expired_magic_link = MagicLink.objects.create(user=self.user, expires_at=timezone.now() - timedelta(minutes=5))
        MagicLink.objects.filter(pk=expired_magic_link.pk).update(token="expired-token")
        expired_magic_link.refresh_from_db()

        retrieved_link = MagicLink.objects.get_valid_link(expired_magic_link.token)
        self.assertIsNone(retrieved_link)

    def test_get_valid_link_with_used_link(self):
        """Test retrieving a used magic link returns None."""
        # Create a used magic link
        used_magic_link = MagicLink.objects.create(
            user=self.user, expires_at=timezone.now() + timedelta(minutes=5), used=True
        )
        MagicLink.objects.filter(pk=used_magic_link.pk).update(token="used-token")
        used_magic_link.refresh_from_db()

        retrieved_link = MagicLink.objects.get_valid_link(used_magic_link.token)
        self.assertIsNone(retrieved_link)

    def test_get_valid_link_with_nonexistent_token(self):
        """Test retrieving a link with a nonexistent token returns None."""
        retrieved_link = MagicLink.objects.get_valid_link("nonexistent-token")
        self.assertIsNone(retrieved_link)


class TestMagicLink(TestCase):
    """Tests for the MagicLink model."""

    def setUp(self):
        """Set up test environment."""
        # Create a user for testing
        from django.contrib.auth import get_user_model

        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")

        # Create a magic link for testing
        self.magic_link = MagicLink.objects.create(user=self.user)
        MagicLink.objects.filter(pk=self.magic_link.pk).update(token="test-token")
        self.magic_link.refresh_from_db()

        # Create an expired magic link
        self.expired_magic_link = MagicLink.objects.create(
            user=self.user, expires_at=timezone.now() - timedelta(minutes=5)
        )
        MagicLink.objects.filter(pk=self.expired_magic_link.pk).update(token="expired-token")
        self.expired_magic_link.refresh_from_db()

        # Create a used magic link
        self.used_magic_link = MagicLink.objects.create(
            user=self.user, expires_at=timezone.now() + timedelta(minutes=5), used=True
        )
        MagicLink.objects.filter(pk=self.used_magic_link.pk).update(token="used-token")
        self.used_magic_link.refresh_from_db()

    def test_create_magic_link(self):
        """Test creating a magic link."""
        self.assertEqual(self.magic_link.user, self.user)
        self.assertEqual(self.magic_link.token, "test-token")
        self.assertIsNotNone(self.magic_link.created_at)
        self.assertGreater(self.magic_link.expires_at, timezone.now())
        self.assertFalse(self.magic_link.used)

    def test_str_method(self):
        """Test the __str__ method."""
        self.assertEqual(str(self.magic_link), f"Magic Link for {self.user}")

    def test_save_method_generates_token(self):
        """Test that save method generates a token if not provided."""
        link = MagicLink(user=self.user)
        link.save()
        self.assertIsNotNone(link.token)
        self.assertGreater(len(link.token), 0)

    def test_save_method_sets_expiration(self):
        """Test that save method sets expiration time if not provided."""
        link = MagicLink(user=self.user)
        link.save()
        self.assertIsNotNone(link.expires_at)
        self.assertGreater(link.expires_at, timezone.now())

    @override_settings(SOLOMON_LINK_EXPIRATION=600)  # 10 minutes
    def test_save_method_respects_custom_expiration(self):
        """Test that save method respects custom expiration time from settings."""
        link = MagicLink(user=self.user)
        before = timezone.now()
        link.save()
        expected_expiration = before + timedelta(seconds=600)
        # Allow for a small time difference due to test execution time
        self.assertLess(abs((link.expires_at - expected_expiration).total_seconds()), 2)

    def test_is_expired_property_with_expired_link(self):
        """Test the is_expired property with an expired link."""
        self.assertTrue(self.expired_magic_link.is_expired)

    def test_is_expired_property_with_valid_link(self):
        """Test the is_expired property with a valid link."""
        self.assertFalse(self.magic_link.is_expired)

    def test_is_valid_property_with_valid_link(self):
        """Test the is_valid property with a valid link."""
        self.assertTrue(self.magic_link.is_valid)

    def test_is_valid_property_with_expired_link(self):
        """Test the is_valid property with an expired link."""
        self.assertFalse(self.expired_magic_link.is_valid)

    def test_is_valid_property_with_used_link(self):
        """Test the is_valid property with a used link."""
        self.assertFalse(self.used_magic_link.is_valid)

    def test_use_method(self):
        """Test the use method."""
        self.assertFalse(self.magic_link.used)
        self.magic_link.use()
        self.assertTrue(self.magic_link.used)
        # Verify it was saved to the database
        self.magic_link.refresh_from_db()
        self.assertTrue(self.magic_link.used)

    def test_save_with_existing_token(self):
        """Test saving a magic link with an existing token."""
        # Create the link first
        link = MagicLink.objects.create(user=self.user)
        # Then update it directly in the database to bypass the save method
        MagicLink.objects.filter(pk=link.pk).update(token="custom-token")
        # Refresh from database to get the updated values
        link.refresh_from_db()
        self.assertEqual(link.token, "custom-token")

        # Test that the token is preserved when saving again
        link.used = True
        link.save(update_fields=["used"])
        link.refresh_from_db()
        self.assertEqual(link.token, "custom-token")

    def test_save_with_existing_expiration(self):
        """Test saving a magic link with an existing expiration time."""
        expiration = timezone.now() + timedelta(hours=2)
        link = MagicLink.objects.create(user=self.user, expires_at=expiration)
        link.refresh_from_db()
        self.assertLess(abs((link.expires_at - expiration).total_seconds()), 1)  # Allow for small time differences

    def test_save_with_existing_token_and_expiration(self):
        """Test saving a magic link with both token and expiration time already set."""
        expiration = timezone.now() + timedelta(hours=2)
        # Create the link first with the expiration time
        link = MagicLink.objects.create(user=self.user, expires_at=expiration)
        # Then update it directly in the database to bypass the save method
        MagicLink.objects.filter(pk=link.pk).update(token="custom-token")
        # Refresh from database to get the updated values
        link.refresh_from_db()
        self.assertEqual(link.token, "custom-token")
        self.assertLess(abs((link.expires_at - expiration).total_seconds()), 1)  # Allow for small time differences
