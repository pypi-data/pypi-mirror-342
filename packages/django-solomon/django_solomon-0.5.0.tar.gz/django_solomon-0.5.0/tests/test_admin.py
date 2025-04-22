from unittest.mock import patch

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase
from django.utils import timezone

from django_solomon.admin import BlacklistedEmailAdmin, MagicLinkAdmin, CustomUserAdmin
from django_solomon.forms import CustomUserCreationForm, CustomUserChangeForm
from django_solomon.models import BlacklistedEmail, MagicLink, CustomUser


class MockSuperUser:
    """A mock superuser for testing admin views."""

    is_active = True
    is_staff = True
    is_superuser = True

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class TestBlacklistedEmailAdmin(TestCase):
    """Tests for the BlacklistedEmailAdmin class."""

    def setUp(self):
        """Set up test environment."""
        # Create fixtures that were previously created by pytest
        self.admin_site = AdminSite()
        self.admin_instance = BlacklistedEmailAdmin(BlacklistedEmail, self.admin_site)
        self.request_factory = RequestFactory()

        # Create a mock request
        self.mock_request = self.request_factory.get("/")
        self.mock_request.user = MockSuperUser()
        # Add messages attribute required by some admin views
        self.mock_request.session = "session"
        messages = FallbackStorage(self.mock_request)
        self.mock_request._messages = messages

        # Create a blacklisted email for tests that need it
        self.blacklisted_email = BlacklistedEmail.objects.create(
            email="blacklisted@example.com", reason="Testing purposes"
        )

    def test_list_display(self):
        """Test that list_display contains the expected fields."""
        self.assertEqual(self.admin_instance.list_display, ("email", "reason", "created_at"))

    def test_list_filter(self):
        """Test that list_filter contains the expected fields."""
        self.assertEqual(self.admin_instance.list_filter, ("created_at",))

    def test_search_fields(self):
        """Test that search_fields contains the expected fields."""
        self.assertEqual(self.admin_instance.search_fields, ("email", "reason"))

    def test_date_hierarchy(self):
        """Test that date_hierarchy is set correctly."""
        self.assertEqual(self.admin_instance.date_hierarchy, "created_at")

    def test_fieldsets(self):
        """Test that fieldsets are configured correctly."""
        self.assertEqual(len(self.admin_instance.fieldsets), 2)
        self.assertEqual(self.admin_instance.fieldsets[0][1]["fields"], ("email", "reason"))
        self.assertEqual(self.admin_instance.fieldsets[1][1]["fields"], ("created_at",))

    def test_readonly_fields(self):
        """Test that readonly_fields contains the expected fields."""
        self.assertEqual(self.admin_instance.readonly_fields, ("created_at",))

    def test_get_queryset(self):
        """Test that get_queryset returns all blacklisted emails."""
        queryset = self.admin_instance.get_queryset(self.mock_request)
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first(), self.blacklisted_email)

    def test_changelist_view(self):
        """Test that the changelist view works correctly."""
        response = self.admin_instance.changelist_view(self.mock_request)
        self.assertEqual(response.status_code, 200)

    def test_add_view(self):
        """Test that the add view works correctly."""
        response = self.admin_instance.add_view(self.mock_request)
        self.assertEqual(response.status_code, 200)

    def test_change_view(self):
        """Test that the change view works correctly."""
        response = self.admin_instance.change_view(self.mock_request, str(self.blacklisted_email.pk))
        self.assertEqual(response.status_code, 200)


class TestMagicLinkAdmin(TestCase):
    """Tests for the MagicLinkAdmin class."""

    def setUp(self):
        """Set up test environment."""
        # Create fixtures that were previously created by pytest
        self.admin_site = AdminSite()
        self.admin_instance = MagicLinkAdmin(MagicLink, self.admin_site)
        self.request_factory = RequestFactory()

        # Create a mock request
        self.mock_request = self.request_factory.get("/")
        self.mock_request.user = MockSuperUser()
        # Add messages attribute required by some admin views
        self.mock_request.session = "session"
        messages = FallbackStorage(self.mock_request)
        self.mock_request._messages = messages

        # Create a user for tests
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")

        # Create magic links for tests
        self.magic_link = MagicLink.objects.create(user=self.user)
        MagicLink.objects.filter(pk=self.magic_link.pk).update(token="test-token")
        self.magic_link.refresh_from_db()

        # Create an expired magic link
        self.expired_magic_link = MagicLink.objects.create(
            user=self.user, expires_at=timezone.now() - timezone.timedelta(minutes=5)
        )
        MagicLink.objects.filter(pk=self.expired_magic_link.pk).update(token="expired-token")
        self.expired_magic_link.refresh_from_db()

        # Create a used magic link
        self.used_magic_link = MagicLink.objects.create(
            user=self.user, expires_at=timezone.now() + timezone.timedelta(minutes=5), used=True
        )
        MagicLink.objects.filter(pk=self.used_magic_link.pk).update(token="used-token")
        self.used_magic_link.refresh_from_db()

    def test_list_display(self):
        """Test that list_display contains the expected fields."""
        self.assertEqual(self.admin_instance.list_display, ("user", "created_at", "expires_at", "used", "is_valid"))

    def test_list_filter(self):
        """Test that list_filter contains the expected fields."""
        self.assertEqual(self.admin_instance.list_filter, ("used", "created_at", "expires_at"))

    def test_search_fields(self):
        """Test that search_fields contains the expected fields."""
        self.assertEqual(self.admin_instance.search_fields, ("user__username", "user__email", "token"))

    def test_readonly_fields(self):
        """Test that readonly_fields contains the expected fields."""
        self.assertEqual(self.admin_instance.readonly_fields, ("id", "token", "created_at", "is_valid"))

    def test_date_hierarchy(self):
        """Test that date_hierarchy is set correctly."""
        self.assertEqual(self.admin_instance.date_hierarchy, "created_at")

    def test_fieldsets(self):
        """Test that fieldsets are configured correctly."""
        self.assertEqual(len(self.admin_instance.fieldsets), 3)
        self.assertEqual(self.admin_instance.fieldsets[0][1]["fields"], ("id", "user", "token"))
        self.assertEqual(self.admin_instance.fieldsets[1][1]["fields"], ("used", "is_valid"))
        self.assertEqual(self.admin_instance.fieldsets[2][1]["fields"], ("created_at", "expires_at"))

    def test_is_valid_method(self):
        """Test the is_valid method."""
        # Valid link
        self.assertTrue(self.admin_instance.is_valid(self.magic_link))

        # Expired link
        self.assertFalse(self.admin_instance.is_valid(self.expired_magic_link))

        # Used link
        self.assertFalse(self.admin_instance.is_valid(self.used_magic_link))

    def test_get_queryset(self):
        """Test that get_queryset returns all magic links."""
        queryset = self.admin_instance.get_queryset(self.mock_request)
        self.assertEqual(queryset.count(), 3)  # We have 3 magic links now
        self.assertIn(self.magic_link, queryset)

    def test_changelist_view(self):
        """Test that the changelist view works correctly."""
        response = self.admin_instance.changelist_view(self.mock_request)
        self.assertEqual(response.status_code, 200)

    def test_add_view(self):
        """Test that the add view works correctly."""
        response = self.admin_instance.add_view(self.mock_request)
        self.assertEqual(response.status_code, 200)

    def test_change_view(self):
        """Test that the change view works correctly."""
        response = self.admin_instance.change_view(self.mock_request, str(self.magic_link.pk))
        self.assertEqual(response.status_code, 200)

    def test_is_valid_with_edge_cases(self):
        """Test the is_valid method with edge cases."""
        # Create a user
        User = get_user_model()
        user = User.objects.create_user(username="edgeuser", email="edge@example.com", password="password123")

        # Mock the token generator to return different tokens
        token_count = 0

        def mock_make_token(user):
            nonlocal token_count
            token_count += 1
            return f"edge-token-{token_count}"

        # Use unittest.mock.patch instead of monkeypatch
        with patch("django.contrib.auth.tokens.default_token_generator.make_token", side_effect=mock_make_token):
            # Edge case 1: Link that expires exactly now
            now = timezone.now()
            edge_link = MagicLink.objects.create(user=user, expires_at=now)
            # The link should be considered expired (not valid)
            self.assertFalse(self.admin_instance.is_valid(edge_link))

            # Edge case 2: Link with no token
            no_token_link = MagicLink.objects.create(user=user)
            MagicLink.objects.filter(pk=no_token_link.pk).update(token="")
            no_token_link.refresh_from_db()
            # The link should still be valid if it's not used and not expired
            self.assertTrue(self.admin_instance.is_valid(no_token_link))


class TestCustomUserAdmin(TestCase):
    """Tests for the CustomUserAdmin class."""

    def setUp(self):
        """Set up test environment."""
        # Create fixtures that were previously created by pytest
        self.admin_site = AdminSite()
        self.admin_instance = CustomUserAdmin(CustomUser, self.admin_site)
        self.request_factory = RequestFactory()

        # Create a mock request
        self.mock_request = self.request_factory.get("/")
        self.mock_request.user = MockSuperUser()
        # Add messages attribute required by some admin views
        self.mock_request.session = "session"
        messages = FallbackStorage(self.mock_request)
        self.mock_request._messages = messages

        # Create a user for tests
        self.user = CustomUser.objects.create_user(email="test@example.com", password="password123")

    def test_add_form(self):
        """Test that add_form is set correctly."""
        self.assertEqual(self.admin_instance.add_form, CustomUserCreationForm)

    def test_form(self):
        """Test that form is set correctly."""
        self.assertEqual(self.admin_instance.form, CustomUserChangeForm)

    def test_model(self):
        """Test that model is set correctly."""
        self.assertEqual(self.admin_instance.model, CustomUser)

    def test_list_display(self):
        """Test that list_display contains the expected fields."""
        self.assertEqual(self.admin_instance.list_display, ("email", "is_superuser", "is_staff", "is_active"))

    def test_list_filter(self):
        """Test that list_filter contains the expected fields."""
        self.assertEqual(self.admin_instance.list_filter, ("is_superuser", "is_staff", "is_active"))

    def test_fieldsets(self):
        """Test that fieldsets are configured correctly."""
        self.assertEqual(len(self.admin_instance.fieldsets), 2)
        self.assertEqual(self.admin_instance.fieldsets[0][1]["fields"], ("email", "password"))
        self.assertEqual(
            self.admin_instance.fieldsets[1][1]["fields"], ("is_staff", "is_active", "groups", "user_permissions")
        )

    def test_add_fieldsets(self):
        """Test that add_fieldsets are configured correctly."""
        self.assertEqual(len(self.admin_instance.add_fieldsets), 1)
        self.assertEqual(
            self.admin_instance.add_fieldsets[0][1]["fields"],
            ("email", "password1", "password2", "is_staff", "is_active", "groups", "user_permissions"),
        )

    def test_search_fields(self):
        """Test that search_fields contains the expected fields."""
        self.assertEqual(self.admin_instance.search_fields, ("email",))

    def test_ordering(self):
        """Test that ordering is set correctly."""
        self.assertEqual(self.admin_instance.ordering, ("email",))

    def test_get_queryset(self):
        """Test that get_queryset returns all users."""
        queryset = self.admin_instance.get_queryset(self.mock_request)
        self.assertEqual(queryset.count(), 1)  # We have 1 user
        self.assertIn(self.user, queryset)

    def test_changelist_view(self):
        """Test that the changelist view works correctly."""
        response = self.admin_instance.changelist_view(self.mock_request)
        self.assertEqual(response.status_code, 200)

    def test_add_view(self):
        """Test that the add view works correctly."""
        response = self.admin_instance.add_view(self.mock_request)
        self.assertEqual(response.status_code, 200)

    def test_change_view(self):
        """Test that the change view works correctly."""
        response = self.admin_instance.change_view(self.mock_request, str(self.user.pk))
        self.assertEqual(response.status_code, 200)
