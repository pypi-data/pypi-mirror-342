import pytest
from django.db import IntegrityError
from django.utils import timezone
from django.test import override_settings
from datetime import timedelta

from django_solomon.models import BlacklistedEmail, MagicLink


@pytest.mark.django_db
class TestBlacklistedEmail:
    """Tests for the BlacklistedEmail model."""

    def test_create_blacklisted_email(self, blacklisted_email):
        """Test creating a blacklisted email."""
        assert blacklisted_email.email == "blacklisted@example.com"
        assert blacklisted_email.reason == "Testing purposes"
        assert blacklisted_email.created_at is not None

    def test_str_method(self, blacklisted_email):
        """Test the __str__ method."""
        assert str(blacklisted_email) == "blacklisted@example.com"

    def test_unique_constraint(self, blacklisted_email):
        """Test that email must be unique."""
        with pytest.raises(IntegrityError):
            BlacklistedEmail.objects.create(email="blacklisted@example.com", reason="Another reason")

    def test_create_without_reason(self):
        """Test creating a blacklisted email without a reason."""
        email = BlacklistedEmail.objects.create(email="no-reason@example.com")
        assert email.email == "no-reason@example.com"
        assert email.reason == ""


@pytest.mark.django_db
class TestMagicLinkManager:
    """Tests for the MagicLinkManager."""

    def test_create_for_user_default_behavior(self, user, monkeypatch):
        """Test creating a magic link for a user with default settings."""
        # Mock the token generator to return different tokens
        token_count = 0

        def mock_make_token(user):
            nonlocal token_count
            token_count += 1
            return f"token-{token_count}"

        monkeypatch.setattr("django.contrib.auth.tokens.default_token_generator.make_token", mock_make_token)

        # Create an initial link
        first_link = MagicLink.objects.create_for_user(user)
        assert first_link.user == user
        assert not first_link.used
        assert first_link.token == "token-1"
        assert first_link.expires_at > timezone.now()

        # Create a second link - the first one should be marked as used
        second_link = MagicLink.objects.create_for_user(user)
        first_link.refresh_from_db()
        assert first_link.used
        assert not second_link.used
        assert second_link.token == "token-2"

    @override_settings(SOLOMON_ONLY_ONE_LINK_ALLOWED=False)
    def test_create_for_user_multiple_links_allowed(self, user, monkeypatch):
        """Test creating multiple magic links for a user when allowed by settings."""
        # Mock the token generator to return different tokens
        token_count = 0

        def mock_make_token(user):
            nonlocal token_count
            token_count += 1
            return f"token-multiple-{token_count}"

        monkeypatch.setattr("django.contrib.auth.tokens.default_token_generator.make_token", mock_make_token)

        # Create an initial link
        first_link = MagicLink.objects.create_for_user(user)
        assert first_link.token == "token-multiple-1"

        # Create a second link - the first one should NOT be marked as used
        second_link = MagicLink.objects.create_for_user(user)
        assert second_link.token == "token-multiple-2"

        first_link.refresh_from_db()

        assert not first_link.used
        assert not second_link.used
        assert MagicLink.objects.filter(user=user, used=False).count() == 2

    def test_get_valid_link_with_valid_link(self, magic_link):
        """Test retrieving a valid magic link."""
        retrieved_link = MagicLink.objects.get_valid_link(magic_link.token)
        assert retrieved_link == magic_link

    def test_get_valid_link_with_expired_link(self, expired_magic_link):
        """Test retrieving an expired magic link returns None."""
        retrieved_link = MagicLink.objects.get_valid_link(expired_magic_link.token)
        assert retrieved_link is None

    def test_get_valid_link_with_used_link(self, used_magic_link):
        """Test retrieving a used magic link returns None."""
        retrieved_link = MagicLink.objects.get_valid_link(used_magic_link.token)
        assert retrieved_link is None

    def test_get_valid_link_with_nonexistent_token(self):
        """Test retrieving a link with a nonexistent token returns None."""
        retrieved_link = MagicLink.objects.get_valid_link("nonexistent-token")
        assert retrieved_link is None


@pytest.mark.django_db
class TestMagicLink:
    """Tests for the MagicLink model."""

    def test_create_magic_link(self, magic_link, user):
        """Test creating a magic link."""
        assert magic_link.user == user
        assert magic_link.token == "test-token"
        assert magic_link.created_at is not None
        assert magic_link.expires_at > timezone.now()
        assert not magic_link.used

    def test_str_method(self, magic_link, user):
        """Test the __str__ method."""
        assert str(magic_link) == f"Magic Link for {user}"

    def test_save_method_generates_token(self, user):
        """Test that save method generates a token if not provided."""
        link = MagicLink(user=user)
        link.save()
        assert link.token is not None
        assert len(link.token) > 0

    def test_save_method_sets_expiration(self, user):
        """Test that save method sets expiration time if not provided."""
        link = MagicLink(user=user)
        link.save()
        assert link.expires_at is not None
        assert link.expires_at > timezone.now()

    @override_settings(SOLOMON_LINK_EXPIRATION=600)  # 10 minutes
    def test_save_method_respects_custom_expiration(self, user):
        """Test that save method respects custom expiration time from settings."""
        link = MagicLink(user=user)
        before = timezone.now()
        link.save()
        expected_expiration = before + timedelta(seconds=600)
        # Allow for a small time difference due to test execution time
        assert abs((link.expires_at - expected_expiration).total_seconds()) < 2

    def test_is_expired_property_with_expired_link(self, expired_magic_link):
        """Test the is_expired property with an expired link."""
        assert expired_magic_link.is_expired

    def test_is_expired_property_with_valid_link(self, magic_link):
        """Test the is_expired property with a valid link."""
        assert not magic_link.is_expired

    def test_is_valid_property_with_valid_link(self, magic_link):
        """Test the is_valid property with a valid link."""
        assert magic_link.is_valid

    def test_is_valid_property_with_expired_link(self, expired_magic_link):
        """Test the is_valid property with an expired link."""
        assert not expired_magic_link.is_valid

    def test_is_valid_property_with_used_link(self, used_magic_link):
        """Test the is_valid property with a used link."""
        assert not used_magic_link.is_valid

    def test_use_method(self, magic_link):
        """Test the use method."""
        assert not magic_link.used
        magic_link.use()
        assert magic_link.used
        # Verify it was saved to the database
        magic_link.refresh_from_db()
        assert magic_link.used

    def test_save_with_existing_token(self, user):
        """Test saving a magic link with an existing token."""
        # Create the link first
        link = MagicLink.objects.create(user=user)
        # Then update it directly in the database to bypass the save method
        MagicLink.objects.filter(pk=link.pk).update(token="custom-token")
        # Refresh from database to get the updated values
        link.refresh_from_db()
        assert link.token == "custom-token"

        # Test that the token is preserved when saving again
        link.used = True
        link.save(update_fields=["used"])
        link.refresh_from_db()
        assert link.token == "custom-token"

    def test_save_with_existing_expiration(self, user):
        """Test saving a magic link with an existing expiration time."""
        expiration = timezone.now() + timedelta(hours=2)
        link = MagicLink.objects.create(user=user, expires_at=expiration)
        link.refresh_from_db()
        assert abs((link.expires_at - expiration).total_seconds()) < 1  # Allow for small time differences

    def test_save_with_existing_token_and_expiration(self, user):
        """Test saving a magic link with both token and expiration time already set."""
        expiration = timezone.now() + timedelta(hours=2)
        # Create the link first with the expiration time
        link = MagicLink.objects.create(user=user, expires_at=expiration)
        # Then update it directly in the database to bypass the save method
        MagicLink.objects.filter(pk=link.pk).update(token="custom-token")
        # Refresh from database to get the updated values
        link.refresh_from_db()
        assert link.token == "custom-token"
        assert abs((link.expires_at - expiration).total_seconds()) < 1  # Allow for small time differences
