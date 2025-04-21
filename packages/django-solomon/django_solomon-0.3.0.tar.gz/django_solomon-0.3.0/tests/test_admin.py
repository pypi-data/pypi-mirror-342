import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory
from django.utils import timezone

from django_solomon.admin import BlacklistedEmailAdmin, MagicLinkAdmin
from django_solomon.models import BlacklistedEmail, MagicLink


class MockSuperUser:
    """A mock superuser for testing admin views."""

    is_active = True
    is_staff = True
    is_superuser = True

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class TestBlacklistedEmailAdmin:
    """Tests for the BlacklistedEmailAdmin class."""

    @pytest.fixture
    def admin_site(self):
        """Create and return an AdminSite instance."""
        return AdminSite()

    @pytest.fixture
    def admin_instance(self, admin_site):
        """Create and return a BlacklistedEmailAdmin instance."""
        return BlacklistedEmailAdmin(BlacklistedEmail, admin_site)

    @pytest.fixture
    def request_factory(self):
        """Create and return a RequestFactory instance."""
        return RequestFactory()

    @pytest.fixture
    def mock_request(self, request_factory):
        """Create and return a mock request with a superuser."""
        request = request_factory.get("/")
        request.user = MockSuperUser()
        # Add messages attribute required by some admin views
        request.session = "session"
        messages = FallbackStorage(request)
        request._messages = messages
        return request

    def test_list_display(self, admin_instance):
        """Test that list_display contains the expected fields."""
        assert admin_instance.list_display == ("email", "reason", "created_at")

    def test_list_filter(self, admin_instance):
        """Test that list_filter contains the expected fields."""
        assert admin_instance.list_filter == ("created_at",)

    def test_search_fields(self, admin_instance):
        """Test that search_fields contains the expected fields."""
        assert admin_instance.search_fields == ("email", "reason")

    def test_date_hierarchy(self, admin_instance):
        """Test that date_hierarchy is set correctly."""
        assert admin_instance.date_hierarchy == "created_at"

    def test_fieldsets(self, admin_instance):
        """Test that fieldsets are configured correctly."""
        assert len(admin_instance.fieldsets) == 2
        assert admin_instance.fieldsets[0][1]["fields"] == ("email", "reason")
        assert admin_instance.fieldsets[1][1]["fields"] == ("created_at",)

    def test_readonly_fields(self, admin_instance):
        """Test that readonly_fields contains the expected fields."""
        assert admin_instance.readonly_fields == ("created_at",)

    @pytest.mark.django_db
    def test_get_queryset(self, admin_instance, mock_request, blacklisted_email):
        """Test that get_queryset returns all blacklisted emails."""
        queryset = admin_instance.get_queryset(mock_request)
        assert queryset.count() == 1
        assert queryset.first() == blacklisted_email

    @pytest.mark.django_db
    def test_changelist_view(self, admin_instance, mock_request, blacklisted_email):
        """Test that the changelist view works correctly."""
        response = admin_instance.changelist_view(mock_request)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_add_view(self, admin_instance, mock_request):
        """Test that the add view works correctly."""
        response = admin_instance.add_view(mock_request)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_change_view(self, admin_instance, mock_request, blacklisted_email):
        """Test that the change view works correctly."""
        response = admin_instance.change_view(mock_request, str(blacklisted_email.pk))
        assert response.status_code == 200


class TestMagicLinkAdmin:
    """Tests for the MagicLinkAdmin class."""

    @pytest.fixture
    def admin_site(self):
        """Create and return an AdminSite instance."""
        return AdminSite()

    @pytest.fixture
    def admin_instance(self, admin_site):
        """Create and return a MagicLinkAdmin instance."""
        return MagicLinkAdmin(MagicLink, admin_site)

    @pytest.fixture
    def request_factory(self):
        """Create and return a RequestFactory instance."""
        return RequestFactory()

    @pytest.fixture
    def mock_request(self, request_factory):
        """Create and return a mock request with a superuser."""
        request = request_factory.get("/")
        request.user = MockSuperUser()
        # Add messages attribute required by some admin views
        request.session = "session"
        messages = FallbackStorage(request)
        request._messages = messages
        return request

    def test_list_display(self, admin_instance):
        """Test that list_display contains the expected fields."""
        assert admin_instance.list_display == ("user", "created_at", "expires_at", "used", "is_valid")

    def test_list_filter(self, admin_instance):
        """Test that list_filter contains the expected fields."""
        assert admin_instance.list_filter == ("used", "created_at", "expires_at")

    def test_search_fields(self, admin_instance):
        """Test that search_fields contains the expected fields."""
        assert admin_instance.search_fields == ("user__username", "user__email", "token")

    def test_readonly_fields(self, admin_instance):
        """Test that readonly_fields contains the expected fields."""
        assert admin_instance.readonly_fields == ("id", "token", "created_at", "is_valid")

    def test_date_hierarchy(self, admin_instance):
        """Test that date_hierarchy is set correctly."""
        assert admin_instance.date_hierarchy == "created_at"

    def test_fieldsets(self, admin_instance):
        """Test that fieldsets are configured correctly."""
        assert len(admin_instance.fieldsets) == 3
        assert admin_instance.fieldsets[0][1]["fields"] == ("id", "user", "token")
        assert admin_instance.fieldsets[1][1]["fields"] == ("used", "is_valid")
        assert admin_instance.fieldsets[2][1]["fields"] == ("created_at", "expires_at")

    @pytest.mark.django_db
    def test_is_valid_method(self, admin_instance, magic_link, expired_magic_link, used_magic_link):
        """Test the is_valid method."""
        # Valid link
        assert admin_instance.is_valid(magic_link) is True

        # Expired link
        assert admin_instance.is_valid(expired_magic_link) is False

        # Used link
        assert admin_instance.is_valid(used_magic_link) is False

    @pytest.mark.django_db
    def test_get_queryset(self, admin_instance, mock_request, magic_link):
        """Test that get_queryset returns all magic links."""
        queryset = admin_instance.get_queryset(mock_request)
        assert queryset.count() == 1
        assert queryset.first() == magic_link

    @pytest.mark.django_db
    def test_changelist_view(self, admin_instance, mock_request, magic_link):
        """Test that the changelist view works correctly."""
        response = admin_instance.changelist_view(mock_request)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_add_view(self, admin_instance, mock_request):
        """Test that the add view works correctly."""
        response = admin_instance.add_view(mock_request)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_change_view(self, admin_instance, mock_request, magic_link):
        """Test that the change view works correctly."""
        response = admin_instance.change_view(mock_request, str(magic_link.pk))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_is_valid_with_edge_cases(self, admin_instance, monkeypatch):
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

        monkeypatch.setattr("django.contrib.auth.tokens.default_token_generator.make_token", mock_make_token)

        # Edge case 1: Link that expires exactly now
        now = timezone.now()
        edge_link = MagicLink.objects.create(user=user, expires_at=now)
        # The link should be considered expired (not valid)
        assert admin_instance.is_valid(edge_link) is False

        # Edge case 2: Link with no token
        no_token_link = MagicLink.objects.create(user=user)
        MagicLink.objects.filter(pk=no_token_link.pk).update(token="")
        no_token_link.refresh_from_db()
        # The link should still be valid if it's not used and not expired
        assert admin_instance.is_valid(no_token_link) is True
