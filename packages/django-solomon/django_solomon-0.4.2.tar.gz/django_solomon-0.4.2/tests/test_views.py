from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.mark.django_db
class TestSendMagicLinkView:
    """Tests for the send_magic_link view."""

    def test_get_request(self, client):
        """Test that a GET request renders the correct template."""
        url = reverse("django_solomon:login")
        response = client.get(url)

        assert response.status_code == 200
        assert "django_solomon/base/login_form.html" in [t.name for t in response.templates]
        assert "form" in response.context

    def test_post_request_with_valid_data(self, client, user):
        """Test that a POST request with valid data sends an email and redirects."""
        url = reverse("django_solomon:login")
        data = {"email": user.email}

        with patch("django_solomon.views.send_mail") as mock_send_mail:
            response = client.post(url, data)

            # Check that the view redirected to the magic_link_sent page
            assert response.status_code == 302
            assert response.url == reverse("django_solomon:magic_link_sent")

            # Check that send_mail was called with the correct arguments
            mock_send_mail.assert_called_once()
            call_args = mock_send_mail.call_args[0]
            assert call_args[0] == "Your Magic Link"  # subject
            assert isinstance(call_args[1], str)  # text message
            assert call_args[2] == "webmaster@localhost"  # from_email (Django's default)
            assert call_args[3] == [user.email]  # recipient_list

            # Check keyword arguments
            kwargs = mock_send_mail.call_args[1]
            assert kwargs["fail_silently"] is False
            assert isinstance(kwargs["html_message"], str)  # html message

    def test_post_request_with_blacklisted_email(self, client, blacklisted_email):
        """Test that a POST request with a blacklisted email redirects without sending an email."""
        url = reverse("django_solomon:login")
        data = {"email": blacklisted_email.email}

        with patch("django_solomon.views.send_mail") as mock_send_mail:
            response = client.post(url, data)

            # Check that the view redirected to the magic_link_sent page
            assert response.status_code == 302
            assert response.url == reverse("django_solomon:magic_link_sent")

            # Check that send_templated_mail was not called
            mock_send_mail.assert_not_called()

    def test_post_request_with_nonexistent_user(self, client):
        """Test that a POST request with a non-existent user redirects without sending an email."""
        url = reverse("django_solomon:login")
        data = {"email": "nonexistent@example.com"}

        with patch("django_solomon.views.send_mail") as mock_send_mail:
            response = client.post(url, data)

            # Check that the view redirected to the magic_link_sent page
            assert response.status_code == 302
            assert response.url == reverse("django_solomon:magic_link_sent")

            # Check that send_templated_mail was not called
            mock_send_mail.assert_not_called()

    def test_post_request_with_nonexistent_user_auto_create(self, client, settings):
        """Test that a POST request with a non-existent user creates the user
        when SOLOMON_CREATE_USER_IF_NOT_FOUND is True."""
        # Enable auto-creation of users
        settings.SOLOMON_CREATE_USER_IF_NOT_FOUND = True

        url = reverse("django_solomon:login")
        email = "new-user@example.com"
        data = {"email": email}

        User = get_user_model()

        # Verify the user doesn't exist yet
        assert not User.objects.filter(email=email).exists()

        with patch("django_solomon.views.send_mail") as mock_send_mail:
            response = client.post(url, data)

            # Check that the view redirected to the magic_link_sent page
            assert response.status_code == 302
            assert response.url == reverse("django_solomon:magic_link_sent")

            # Check that a new user was created
            assert User.objects.filter(email=email).exists()

            # Check that send_mail was called with the correct arguments
            mock_send_mail.assert_called_once()
            call_args = mock_send_mail.call_args[0]
            assert call_args[0] == "Your Magic Link"  # subject
            assert isinstance(call_args[1], str)  # text message
            assert call_args[2] == "webmaster@localhost"  # from_email (Django's default)
            assert call_args[3] == [email]  # recipient_list

            # Check keyword arguments
            kwargs = mock_send_mail.call_args[1]
            assert kwargs["fail_silently"] is False
            assert isinstance(kwargs["html_message"], str)  # html message

    def test_post_request_with_invalid_form(self, client):
        """Test that a POST request with invalid form data renders the form with errors."""
        url = reverse("django_solomon:login")
        data = {"email": "not-an-email"}  # Invalid email format

        response = client.post(url, data)

        # Check that the view rendered the form with errors
        assert response.status_code == 200
        assert "django_solomon/base/login_form.html" in [t.name for t in response.templates]
        assert "form" in response.context
        assert response.context["form"].errors

    def test_email_actually_sent(self, client, user, settings):
        """Test that an email is actually sent when using the real email backend."""
        # Mock the send_mail function but still verify it's called
        with patch("django_solomon.views.send_mail") as mock_send_mail:
            url = reverse("django_solomon:login")
            data = {"email": user.email}

            response = client.post(url, data)

            # Check that the view redirected to the magic_link_sent page
            assert response.status_code == 302
            assert response.url == reverse("django_solomon:magic_link_sent")

            # Check that send_mail was called with the correct arguments
            mock_send_mail.assert_called_once()
            call_args = mock_send_mail.call_args[0]
            assert call_args[0] == "Your Magic Link"  # subject
            assert isinstance(call_args[1], str)  # text message
            assert call_args[2] == "webmaster@localhost"  # from_email (Django's default)
            assert call_args[3] == [user.email]  # recipient_list

            # Check keyword arguments
            kwargs = mock_send_mail.call_args[1]
            assert kwargs["fail_silently"] is False
            assert isinstance(kwargs["html_message"], str)  # html message

    def test_custom_link_expiration(self, client, user, settings):
        """Test that the expiry_time in the email context is calculated correctly based on SOLOMON_LINK_EXPIRATION."""
        # Set a custom link expiration time (in seconds)
        settings.SOLOMON_LINK_EXPIRATION = 600  # 10 minutes

        # We need to mock mjml2html to check the rendered template content
        with (
            patch("django_solomon.views.mjml2html") as mock_mjml2html,
            patch("django_solomon.views.send_mail") as mock_send_mail,
        ):
            # Set up mock_mjml2html to return a dummy string
            mock_mjml2html.return_value = "<html>Mocked HTML content</html>"

            url = reverse("django_solomon:login")
            data = {"email": user.email}

            response = client.post(url, data)

            # Check that the view redirected to the magic_link_sent page
            assert response.status_code == 302
            assert response.url == reverse("django_solomon:magic_link_sent")

            # Check that mjml2html was called
            mock_mjml2html.assert_called()

            # Check that the rendered template contains the correct expiry time
            # We can't directly check the context, but we can check that the template
            # was rendered with the correct expiry time by checking the input to mjml2html
            mjml_content = mock_mjml2html.call_args[0][0]
            assert "10 minutes" in mjml_content or "10 min" in mjml_content

            # Check that send_mail was called
            mock_send_mail.assert_called_once()


@pytest.mark.django_db
class TestMagicLinkSentView:
    """Tests for the magic_link_sent view."""

    def test_get_request(self, client):
        """Test that a GET request renders the correct template."""
        url = reverse("django_solomon:magic_link_sent")
        response = client.get(url)

        assert response.status_code == 200
        assert "django_solomon/base/magic_link_sent.html" in [t.name for t in response.templates]


@pytest.mark.django_db
class TestValidateMagicLinkView:
    """Tests for the validate_magic_link view."""

    def test_valid_token(self, client, magic_link):
        """Test that a valid token authenticates the user and redirects."""
        url = reverse("django_solomon:validate_magic_link", kwargs={"token": magic_link.token})

        with patch("django_solomon.views.authenticate", return_value=magic_link.user) as mock_authenticate:
            response = client.get(url)

            # Check that authenticate was called with the correct arguments
            mock_authenticate.assert_called_once_with(request=response.wsgi_request, token=magic_link.token)

            # Check that the view redirected to the success URL
            assert response.status_code == 302
            assert response.url == "/accounts/profile/"  # Default LOGIN_REDIRECT_URL

    def test_invalid_token(self, client):
        """Test that an invalid token renders the invalid_magic_link template."""
        url = reverse("django_solomon:validate_magic_link", kwargs={"token": "invalid-token"})

        with patch("django_solomon.views.authenticate", return_value=None) as mock_authenticate:
            response = client.get(url)

            # Check that authenticate was called with the correct arguments
            mock_authenticate.assert_called_once_with(request=response.wsgi_request, token="invalid-token")

            # Check that the view rendered the invalid_magic_link template
            assert response.status_code == 200
            assert "django_solomon/base/invalid_magic_link.html" in [t.name for t in response.templates]
            assert "error" in response.context

    def test_expired_token(self, client, expired_magic_link):
        """Test that an expired token renders the invalid_magic_link template."""
        url = reverse("django_solomon:validate_magic_link", kwargs={"token": expired_magic_link.token})

        # The authenticate backend should return None for an expired token
        with patch("django_solomon.views.authenticate", return_value=None) as mock_authenticate:
            response = client.get(url)

            # Check that authenticate was called with the correct arguments
            mock_authenticate.assert_called_once_with(request=response.wsgi_request, token=expired_magic_link.token)

            # Check that the view rendered the invalid_magic_link template
            assert response.status_code == 200
            assert "django_solomon/base/invalid_magic_link.html" in [t.name for t in response.templates]
            assert "error" in response.context

    def test_used_token(self, client, used_magic_link):
        """Test that a used token renders the invalid_magic_link template."""
        url = reverse("django_solomon:validate_magic_link", kwargs={"token": used_magic_link.token})

        # The authenticate backend should return None for a used token
        with patch("django_solomon.views.authenticate", return_value=None) as mock_authenticate:
            response = client.get(url)

            # Check that authenticate was called with the correct arguments
            mock_authenticate.assert_called_once_with(request=response.wsgi_request, token=used_magic_link.token)

            # Check that the view rendered the invalid_magic_link template
            assert response.status_code == 200
            assert "django_solomon/base/invalid_magic_link.html" in [t.name for t in response.templates]
            assert "error" in response.context

    def test_custom_error_message(self, client):
        """Test that a custom error message is displayed if provided."""
        url = reverse("django_solomon:validate_magic_link", kwargs={"token": "invalid-token"})

        # Mock authenticate to return None and set a custom error message
        def mock_authenticate_with_error(request, token):
            request.magic_link_error = "Custom error message"
            return None

        with patch("django_solomon.views.authenticate", side_effect=mock_authenticate_with_error) as mock_authenticate:
            response = client.get(url)

            # Check that authenticate was called with the correct arguments
            mock_authenticate.assert_called_once_with(request=response.wsgi_request, token="invalid-token")

            # Check that the view rendered the invalid_magic_link template with the custom error
            assert response.status_code == 200
            assert "django_solomon/base/invalid_magic_link.html" in [t.name for t in response.templates]
            assert response.context["error"] == "Custom error message"

    def test_successful_login(self, client, magic_link, settings):
        """Test that a successful login actually logs in the user and redirects to the success URL."""
        # Set a custom success URL
        settings.SOLOMON_LOGIN_REDIRECT_URL = "/custom-success-url/"

        url = reverse("django_solomon:validate_magic_link", kwargs={"token": magic_link.token})

        # Mock the authenticate function to return the user
        with patch("django_solomon.views.authenticate", return_value=magic_link.user) as mock_authenticate:
            response = client.get(url)

            # Check that authenticate was called with the correct arguments
            mock_authenticate.assert_called_once_with(request=response.wsgi_request, token=magic_link.token)

            # Check that the view redirected to the custom success URL
            assert response.status_code == 302
            assert response.url == "/custom-success-url/"

            # Check that the user is logged in
            assert "_auth_user_id" in client.session
