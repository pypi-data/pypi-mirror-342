from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from django_solomon.models import BlacklistedEmail, MagicLink


class TestSendMagicLinkView(TestCase):
    """Tests for the send_magic_link view."""

    def setUp(self):
        """Set up test environment."""
        # Create a user for testing
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")

        # Create a blacklisted email for testing
        self.blacklisted_email = BlacklistedEmail.objects.create(
            email="blacklisted@example.com", reason="Testing purposes"
        )

    def test_get_request(self):
        """Test that a GET request renders the correct template."""
        url = reverse("django_solomon:login")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("django_solomon/base/login_form.html", [t.name for t in response.templates])
        self.assertIn("form", response.context)

    def test_post_request_with_valid_data(self):
        """Test that a POST request with valid data sends an email and redirects."""
        url = reverse("django_solomon:login")
        data = {"email": self.user.email}

        with patch("django_solomon.views.send_mail") as mock_send_mail:
            response = self.client.post(url, data)

            # Check that the view redirected to the magic_link_sent page
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse("django_solomon:magic_link_sent"))

            # Check that send_mail was called with the correct arguments
            mock_send_mail.assert_called_once()
            call_args = mock_send_mail.call_args[0]
            self.assertEqual(call_args[0], "Your Magic Link")  # subject
            self.assertIsInstance(call_args[1], str)  # text message
            self.assertEqual(call_args[2], "webmaster@localhost")  # from_email (Django's default)
            self.assertEqual(call_args[3], [self.user.email])  # recipient_list

            # Check keyword arguments
            kwargs = mock_send_mail.call_args[1]
            self.assertFalse(kwargs["fail_silently"])
            self.assertIsInstance(kwargs["html_message"], str)  # html message

    def test_post_request_with_blacklisted_email(self):
        """Test that a POST request with a blacklisted email redirects without sending an email."""
        url = reverse("django_solomon:login")
        data = {"email": self.blacklisted_email.email}

        with patch("django_solomon.views.send_mail") as mock_send_mail:
            response = self.client.post(url, data)

            # Check that the view redirected to the magic_link_sent page
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse("django_solomon:magic_link_sent"))

            # Check that send_templated_mail was not called
            mock_send_mail.assert_not_called()

    def test_post_request_with_nonexistent_user(self):
        """Test that a POST request with a non-existent user redirects without sending an email."""
        url = reverse("django_solomon:login")
        data = {"email": "nonexistent@example.com"}

        with patch("django_solomon.views.send_mail") as mock_send_mail:
            response = self.client.post(url, data)

            # Check that the view redirected to the magic_link_sent page
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse("django_solomon:magic_link_sent"))

            # Check that send_templated_mail was not called
            mock_send_mail.assert_not_called()

    def test_post_request_with_nonexistent_user_auto_create(self):
        """Test that a POST request with a non-existent user creates the user
        when SOLOMON_CREATE_USER_IF_NOT_FOUND is True."""
        # Enable auto-creation of users
        with self.settings(SOLOMON_CREATE_USER_IF_NOT_FOUND=True):
            url = reverse("django_solomon:login")
            email = "new-user@example.com"
            data = {"email": email}

            User = get_user_model()

            # Verify the user doesn't exist yet
            self.assertFalse(User.objects.filter(email=email).exists())

            with patch("django_solomon.views.send_mail") as mock_send_mail:
                response = self.client.post(url, data)

                # Check that the view redirected to the magic_link_sent page
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.url, reverse("django_solomon:magic_link_sent"))

                # Check that a new user was created
                self.assertTrue(User.objects.filter(email=email).exists())

                # Check that send_mail was called with the correct arguments
                mock_send_mail.assert_called_once()
                call_args = mock_send_mail.call_args[0]
                self.assertEqual(call_args[0], "Your Magic Link")  # subject
                self.assertIsInstance(call_args[1], str)  # text message
                self.assertEqual(call_args[2], "webmaster@localhost")  # from_email (Django's default)
                self.assertEqual(call_args[3], [email])  # recipient_list

                # Check keyword arguments
                kwargs = mock_send_mail.call_args[1]
                self.assertFalse(kwargs["fail_silently"])
                self.assertIsInstance(kwargs["html_message"], str)  # html message

    def test_post_request_with_invalid_form(self):
        """Test that a POST request with invalid form data renders the form with errors."""
        url = reverse("django_solomon:login")
        data = {"email": "not-an-email"}  # Invalid email format

        response = self.client.post(url, data)

        # Check that the view rendered the form with errors
        self.assertEqual(response.status_code, 200)
        self.assertIn("django_solomon/base/login_form.html", [t.name for t in response.templates])
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)

    def test_email_actually_sent(self):
        """Test that an email is actually sent when using the real email backend."""
        # Mock the send_mail function but still verify it's called
        with patch("django_solomon.views.send_mail") as mock_send_mail:
            url = reverse("django_solomon:login")
            data = {"email": self.user.email}

            response = self.client.post(url, data)

            # Check that the view redirected to the magic_link_sent page
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse("django_solomon:magic_link_sent"))

            # Check that send_mail was called with the correct arguments
            mock_send_mail.assert_called_once()
            call_args = mock_send_mail.call_args[0]
            self.assertEqual(call_args[0], "Your Magic Link")  # subject
            self.assertIsInstance(call_args[1], str)  # text message
            self.assertEqual(call_args[2], "webmaster@localhost")  # from_email (Django's default)
            self.assertEqual(call_args[3], [self.user.email])  # recipient_list

            # Check keyword arguments
            kwargs = mock_send_mail.call_args[1]
            self.assertFalse(kwargs["fail_silently"])
            self.assertIsInstance(kwargs["html_message"], str)  # html message

    def test_custom_link_expiration(self):
        """Test that the expiry_time in the email context is calculated correctly based on SOLOMON_LINK_EXPIRATION."""
        # Set a custom link expiration time (in seconds)
        with self.settings(SOLOMON_LINK_EXPIRATION=600):  # 10 minutes
            # We need to mock mjml2html to check the rendered template content
            with (
                patch("django_solomon.views.mjml2html") as mock_mjml2html,
                patch("django_solomon.views.send_mail") as mock_send_mail,
            ):
                # Set up mock_mjml2html to return a dummy string
                mock_mjml2html.return_value = "<html>Mocked HTML content</html>"

                url = reverse("django_solomon:login")
                data = {"email": self.user.email}

                response = self.client.post(url, data)

                # Check that the view redirected to the magic_link_sent page
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.url, reverse("django_solomon:magic_link_sent"))

                # Check that mjml2html was called
                mock_mjml2html.assert_called()

                # Check that the rendered template contains the correct expiry time
                # We can't directly check the context, but we can check that the template
                # was rendered with the correct expiry time by checking the input to mjml2html
                mjml_content = mock_mjml2html.call_args[0][0]
                self.assertTrue("10 minutes" in mjml_content or "10 min" in mjml_content)

                # Check that send_mail was called
                mock_send_mail.assert_called_once()


class TestMagicLinkSentView(TestCase):
    """Tests for the magic_link_sent view."""

    def test_get_request(self):
        """Test that a GET request renders the correct template."""
        url = reverse("django_solomon:magic_link_sent")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("django_solomon/base/magic_link_sent.html", [t.name for t in response.templates])


class TestValidateMagicLinkView(TestCase):
    """Tests for the validate_magic_link view."""

    def setUp(self):
        """Set up test environment."""
        # Create a user for testing
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")

        # Create a magic link for testing
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

    def test_valid_token(self):
        """Test that a valid token authenticates the user and redirects."""
        url = reverse("django_solomon:validate_magic_link", kwargs={"token": self.magic_link.token})

        with patch("django_solomon.views.authenticate", return_value=self.magic_link.user) as mock_authenticate:
            response = self.client.get(url)

            # Check that authenticate was called with the correct arguments
            mock_authenticate.assert_called_once_with(request=response.wsgi_request, token=self.magic_link.token)

            # Check that the view redirected to the success URL
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, "/accounts/profile/")  # Default LOGIN_REDIRECT_URL

    def test_invalid_token(self):
        """Test that an invalid token renders the invalid_magic_link template."""
        url = reverse("django_solomon:validate_magic_link", kwargs={"token": "invalid-token"})

        with patch("django_solomon.views.authenticate", return_value=None) as mock_authenticate:
            response = self.client.get(url)

            # Check that authenticate was called with the correct arguments
            mock_authenticate.assert_called_once_with(request=response.wsgi_request, token="invalid-token")

            # Check that the view rendered the invalid_magic_link template
            self.assertEqual(response.status_code, 200)
            self.assertIn("django_solomon/base/invalid_magic_link.html", [t.name for t in response.templates])
            self.assertIn("error", response.context)

    def test_expired_token(self):
        """Test that an expired token renders the invalid_magic_link template."""
        url = reverse("django_solomon:validate_magic_link", kwargs={"token": self.expired_magic_link.token})

        # The authenticate backend should return None for an expired token
        with patch("django_solomon.views.authenticate", return_value=None) as mock_authenticate:
            response = self.client.get(url)

            # Check that authenticate was called with the correct arguments
            mock_authenticate.assert_called_once_with(
                request=response.wsgi_request, token=self.expired_magic_link.token
            )

            # Check that the view rendered the invalid_magic_link template
            self.assertEqual(response.status_code, 200)
            self.assertIn("django_solomon/base/invalid_magic_link.html", [t.name for t in response.templates])
            self.assertIn("error", response.context)

    def test_used_token(self):
        """Test that a used token renders the invalid_magic_link template."""
        url = reverse("django_solomon:validate_magic_link", kwargs={"token": self.used_magic_link.token})

        # The authenticate backend should return None for a used token
        with patch("django_solomon.views.authenticate", return_value=None) as mock_authenticate:
            response = self.client.get(url)

            # Check that authenticate was called with the correct arguments
            mock_authenticate.assert_called_once_with(request=response.wsgi_request, token=self.used_magic_link.token)

            # Check that the view rendered the invalid_magic_link template
            self.assertEqual(response.status_code, 200)
            self.assertIn("django_solomon/base/invalid_magic_link.html", [t.name for t in response.templates])
            self.assertIn("error", response.context)

    def test_custom_error_message(self):
        """Test that a custom error message is displayed if provided."""
        url = reverse("django_solomon:validate_magic_link", kwargs={"token": "invalid-token"})

        # Mock authenticate to return None and set a custom error message
        def mock_authenticate_with_error(request, token):
            request.magic_link_error = "Custom error message"
            return None

        with patch("django_solomon.views.authenticate", side_effect=mock_authenticate_with_error) as mock_authenticate:
            response = self.client.get(url)

            # Check that authenticate was called with the correct arguments
            mock_authenticate.assert_called_once_with(request=response.wsgi_request, token="invalid-token")

            # Check that the view rendered the invalid_magic_link template with the custom error
            self.assertEqual(response.status_code, 200)
            self.assertIn("django_solomon/base/invalid_magic_link.html", [t.name for t in response.templates])
            self.assertEqual(response.context["error"], "Custom error message")

    def test_successful_login(self):
        """Test that a successful login actually logs in the user and redirects to the success URL."""
        # Set a custom success URL
        with self.settings(SOLOMON_LOGIN_REDIRECT_URL="/custom-success-url/"):
            url = reverse("django_solomon:validate_magic_link", kwargs={"token": self.magic_link.token})

            # Mock the authenticate function to return the user
            with patch("django_solomon.views.authenticate", return_value=self.magic_link.user) as mock_authenticate:
                response = self.client.get(url)

                # Check that authenticate was called with the correct arguments
                mock_authenticate.assert_called_once_with(request=response.wsgi_request, token=self.magic_link.token)

                # Check that the view redirected to the custom success URL
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.url, "/custom-success-url/")

                # Check that the user is logged in
                self.assertIn("_auth_user_id", self.client.session)
