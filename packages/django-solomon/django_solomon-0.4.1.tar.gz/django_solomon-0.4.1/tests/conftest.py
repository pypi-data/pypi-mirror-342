import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from django_solomon.models import BlacklistedEmail, MagicLink


@pytest.fixture
def user():
    """Create and return a user for testing."""
    User = get_user_model()
    return User.objects.create_user(username="testuser", email="test@example.com", password="password123")


@pytest.fixture
def blacklisted_email():
    """Create and return a blacklisted email for testing."""
    return BlacklistedEmail.objects.create(email="blacklisted@example.com", reason="Testing purposes")


@pytest.fixture
def magic_link(user):
    """Create and return a magic link for testing."""
    # Create the link first
    link = MagicLink.objects.create(user=user)
    # Then update it directly in the database to bypass the save method
    MagicLink.objects.filter(pk=link.pk).update(token="test-token")
    # Refresh from database to get the updated values
    link.refresh_from_db()
    return link


@pytest.fixture
def expired_magic_link(user):
    """Create and return an expired magic link for testing."""
    # Create the link first with an expired expiration time
    link = MagicLink.objects.create(user=user, expires_at=timezone.now() - timedelta(minutes=5))
    # Then update it directly in the database to bypass the save method
    MagicLink.objects.filter(pk=link.pk).update(token="expired-token")
    # Refresh from database to get the updated values
    link.refresh_from_db()
    return link


@pytest.fixture
def used_magic_link(user):
    """Create and return a used magic link for testing."""
    # Create the link first
    link = MagicLink.objects.create(user=user, expires_at=timezone.now() + timedelta(minutes=5), used=True)
    # Then update it directly in the database to bypass the save method
    MagicLink.objects.filter(pk=link.pk).update(token="used-token")
    # Refresh from database to get the updated values
    link.refresh_from_db()
    return link
