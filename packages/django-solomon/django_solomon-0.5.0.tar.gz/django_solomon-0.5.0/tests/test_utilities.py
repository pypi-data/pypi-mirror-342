import socket
from unittest.mock import patch, MagicMock

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import override_settings, TestCase

from django_solomon.utilities import (
    get_user_by_email,
    create_user_from_email,
    get_ip_from_hostname,
    get_client_ip,
    anonymize_ip,
)


class TestGetUserByEmail(TestCase):
    """Tests for the get_user_by_email function."""

    def setUp(self):
        """Set up test environment."""
        # Create a user for testing
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")

    def test_get_user_by_email_with_existing_user(self):
        """Test getting a user by email when the user exists."""
        found_user = get_user_by_email("test@example.com")
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.email, "test@example.com")
        self.assertEqual(found_user.username, "test@example.com")

    def test_get_user_by_email_with_nonexistent_email(self):
        """Test getting a user by email when the email doesn't exist."""
        found_user = get_user_by_email("nonexistent@example.com")
        self.assertIsNone(found_user)

    def test_get_user_by_email_with_custom_email_field(self):
        """Test getting a user by email when the user model has a custom EMAIL_FIELD."""
        user_model = get_user_model()

        # Mock the User model to have a custom EMAIL_FIELD
        with patch.object(user_model, "EMAIL_FIELD", "custom_email"):
            # Mock hasattr to return True for both EMAIL_FIELD and custom_email
            def mock_hasattr(obj, attr):
                if attr == "EMAIL_FIELD" or attr == "custom_email":
                    return True
                return False

            with patch("django_solomon.utilities.hasattr", mock_hasattr):
                # Mock the User.objects.get method to return a user
                mock_user = MagicMock()
                mock_user.custom_email = "custom@example.com"

                with patch.object(user_model.objects, "get", return_value=mock_user):
                    found_user = get_user_by_email("custom@example.com")
                    self.assertIsNotNone(found_user)
                    self.assertEqual(found_user.custom_email, "custom@example.com")

    def test_get_user_by_email_with_no_email_field(self):
        """Test getting a user by email when the user model doesn't have an email field."""
        # Mock hasattr to return False for both EMAIL_FIELD and 'email'
        with patch("django_solomon.utilities.hasattr", return_value=False):
            found_user = get_user_by_email("test@example.com")
            self.assertIsNone(found_user)

    def test_get_user_by_email_with_custom_field_fallback_to_nonexistent_email(self):
        """Test getting a user by email when a custom field doesn't exist and fallback to 'email' also doesn't exist."""
        User = get_user_model()

        # This is a more complex scenario:
        # 1. User model has EMAIL_FIELD attribute
        # 2. The value of EMAIL_FIELD is 'custom_field'
        # 3. 'custom_field' doesn't exist on the model
        # 4. We fall back to 'email'
        # 5. 'email' also doesn't exist on the model

        # Use a counter to track the number of calls to hasattr
        call_count = 0

        def mock_hasattr(obj, attr):
            nonlocal call_count
            call_count += 1

            # First call: hasattr(user_model, "EMAIL_FIELD") -> True
            if call_count == 1 and attr == "EMAIL_FIELD":
                return True
            # Second call: hasattr(user_model, "custom_field") -> False
            elif call_count == 2 and attr == "custom_field":
                return False
            # Third call: hasattr(user_model, "email") -> False
            elif call_count == 3 and attr == "email":
                return False
            return False

        # Mock EMAIL_FIELD to be a custom field
        with patch.object(User, "EMAIL_FIELD", "custom_field"):
            with patch("django_solomon.utilities.hasattr", mock_hasattr):
                found_user = get_user_by_email("test@example.com")
                self.assertIsNone(found_user)
                # Verify that hasattr was called 3 times
                self.assertEqual(call_count, 3)

    def test_get_user_by_email_branch_coverage(self):
        """Test specifically targeting the branch at line 37->42 in utilities.py."""
        # Import the module directly to patch it
        import django_solomon.utilities as utils

        # Create a mock user model
        mock_user_model = MagicMock()
        mock_user_model.__name__ = "MockUserModel"

        # Create a mock for get_user_model that returns our mock user model
        with patch("django_solomon.utilities.get_user_model", return_value=mock_user_model):
            # First, make hasattr return False for both EMAIL_FIELD and email
            # This will cause the function to return None at line 39
            with patch.object(utils, "hasattr", return_value=False):
                found_user = utils.get_user_by_email("test@example.com")
                self.assertIsNone(found_user)

    def test_get_user_by_email_with_fallback_field_exists(self):
        """Test getting a user by email when the original field doesn't exist but the fallback field does."""
        # Import the module directly to patch it
        import django_solomon.utilities as utils

        # Create a mock user model
        mock_user_model = MagicMock()
        mock_user_model.__name__ = "MockUserModel"
        mock_user_model.DoesNotExist = Exception

        # Create a mock user to be returned by the query
        mock_user = MagicMock()
        mock_user.email = "test@example.com"

        # Mock the objects.get method to return our mock user
        mock_user_model.objects.get.return_value = mock_user

        # Create a sequence of responses for hasattr
        call_count = 0

        def mock_hasattr(obj, attr):
            nonlocal call_count
            call_count += 1

            # First call: hasattr(user_model, "EMAIL_FIELD") -> True
            if call_count == 1 and attr == "EMAIL_FIELD":
                return True
            # Second call: hasattr(user_model, "custom_field") -> False
            elif call_count == 2 and attr == "custom_field":
                return False
            # Third call: hasattr(user_model, "email") -> True (this is the key difference)
            elif call_count == 3 and attr == "email":
                return True
            return False

        # Create a mock for get_user_model that returns our mock user model
        with patch("django_solomon.utilities.get_user_model", return_value=mock_user_model):
            # Mock EMAIL_FIELD to be a custom field
            with patch.object(mock_user_model, "EMAIL_FIELD", "custom_field"):
                # Mock hasattr to return our sequence of responses
                with patch.object(utils, "hasattr", mock_hasattr):
                    found_user = utils.get_user_by_email("test@example.com")
                    self.assertIsNotNone(found_user)
                    self.assertEqual(found_user.email, "test@example.com")
                    # Verify that hasattr was called 3 times
                    self.assertEqual(call_count, 3)

    def test_get_user_by_email_with_fallback_to_email(self):
        """Test getting a user by email when EMAIL_FIELD doesn't exist but 'email' does."""
        User = get_user_model()

        # Create a mock user to be returned by the query
        mock_user = MagicMock()
        mock_user.email = "test@example.com"

        # Mock hasattr to return False for EMAIL_FIELD but True for 'email'
        def mock_hasattr(obj, attr):
            if attr == "EMAIL_FIELD":
                return False
            elif attr == "email":
                return True
            return False

        with patch("django_solomon.utilities.hasattr", mock_hasattr):
            # Mock the User.objects.get method to return our mock user
            with patch.object(User.objects, "get", return_value=mock_user):
                found_user = get_user_by_email("test@example.com")
                self.assertIsNotNone(found_user)
                self.assertEqual(found_user.email, "test@example.com")

    def test_get_user_by_email_with_exception(self):
        """Test getting a user by email when an exception occurs."""
        User = get_user_model()

        # Mock User.objects.get to raise an exception
        with patch.object(User.objects, "get", side_effect=Exception("Test exception")):
            found_user = get_user_by_email("test@example.com")
            self.assertIsNone(found_user)

    def test_get_user_by_email_with_does_not_exist_exception(self):
        """Test getting a user by email when DoesNotExist exception occurs."""
        # This is already tested in test_get_user_by_email_with_nonexistent_email
        # but we'll test it explicitly here for completeness
        found_user = get_user_by_email("nonexistent@example.com")
        self.assertIsNone(found_user)


class TestCreateUserFromEmail(TestCase):
    """Tests for the create_user_from_email function."""

    def test_create_user_from_email_without_email_field(self):
        """Test creating a user when the user model doesn't have EMAIL_FIELD."""
        email = "no_email_field@example.com"
        user_model = get_user_model()

        # Mock hasattr to return False for EMAIL_FIELD
        def mock_hasattr(obj, attr):
            if attr == "EMAIL_FIELD":
                return False
            return hasattr(obj, attr)

        with patch("django_solomon.utilities.hasattr", mock_hasattr):
            # Mock the create_user method to capture the kwargs
            create_user_kwargs = {}
            original_create_user = user_model.objects.create_user

            def mock_create_user(**kwargs):
                # Save the kwargs for later assertion
                nonlocal create_user_kwargs
                create_user_kwargs = kwargs.copy()

                return original_create_user(
                    username=kwargs.get("username"), email=kwargs.get("email"), password=kwargs.get("password")
                )

            with patch.object(user_model.objects, "create_user", side_effect=mock_create_user):
                user = create_user_from_email(email)

                self.assertIsNotNone(user)
                self.assertEqual(user.email, email)
                self.assertEqual(user.username, email)

                # Verify that only the standard fields were included in the kwargs
                self.assertIn("username", create_user_kwargs)
                self.assertIn("email", create_user_kwargs)
                self.assertIn("password", create_user_kwargs)
                self.assertEqual(len(create_user_kwargs), 3)  # Only these three fields

    def test_create_user_from_email_standard(self):
        """Test creating a user with a standard email."""
        email = "newuser@example.com"
        user = create_user_from_email(email)

        self.assertIsNotNone(user)
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, email)

        # Verify the user was actually created in the database
        User = get_user_model()
        db_user = User.objects.get(email=email)
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.email, email)
        self.assertEqual(db_user.username, email)

        # We don't check if the password is unusable because Django's create_user
        # might hash the already hashed password, making it usable

    def test_create_user_from_email_with_email_field_as_email(self):
        """Test creating a user when the user model's EMAIL_FIELD is 'email'."""
        email = "standard@example.com"
        user_model = get_user_model()

        # Mock the User model to have EMAIL_FIELD as "email"
        with patch.object(user_model, "EMAIL_FIELD", "email"):
            # Mock hasattr to return True for EMAIL_FIELD
            def mock_hasattr(obj, attr):
                if attr == "EMAIL_FIELD":
                    return True
                return hasattr(obj, attr)

            with patch("django_solomon.utilities.hasattr", mock_hasattr):
                # Mock the create_user method to capture the kwargs
                create_user_kwargs = {}
                original_create_user = user_model.objects.create_user

                def mock_create_user(**kwargs):
                    # Save the kwargs for later assertion
                    nonlocal create_user_kwargs
                    create_user_kwargs = kwargs.copy()

                    return original_create_user(
                        username=kwargs.get("username"), email=kwargs.get("email"), password=kwargs.get("password")
                    )

                with patch.object(user_model.objects, "create_user", side_effect=mock_create_user):
                    user = create_user_from_email(email)

                    self.assertIsNotNone(user)
                    self.assertEqual(user.email, email)
                    self.assertEqual(user.username, email)

                    # Verify that only the standard fields were included in the kwargs
                    # This ensures the branch where email_field == "email" is covered
                    self.assertIn("username", create_user_kwargs)
                    self.assertIn("email", create_user_kwargs)
                    self.assertIn("password", create_user_kwargs)
                    self.assertEqual(len(create_user_kwargs), 3)  # Only these three fields

    def test_create_user_from_email_with_custom_email_field(self):
        """Test creating a user when the user model has a custom EMAIL_FIELD."""
        email = "custom@example.com"
        user_model = get_user_model()

        # Mock the User model to have a custom EMAIL_FIELD
        with patch.object(user_model, "EMAIL_FIELD", "custom_email"):
            # Mock hasattr to return True for EMAIL_FIELD
            def mock_hasattr(obj, attr):
                if attr == "EMAIL_FIELD" or attr == "custom_email":
                    return True
                return hasattr(obj, attr)

            with patch("django_solomon.utilities.hasattr", mock_hasattr):
                # Mock the create_user method to capture the kwargs
                create_user_kwargs = {}
                original_create_user = user_model.objects.create_user

                def mock_create_user(**kwargs):
                    # Save the kwargs for later assertion
                    nonlocal create_user_kwargs
                    create_user_kwargs = kwargs.copy()

                    user = original_create_user(
                        username=kwargs.get("username"), email=kwargs.get("email"), password=kwargs.get("password")
                    )
                    # Add the custom email field
                    user.custom_email = kwargs.get("custom_email")
                    return user

                with patch.object(user_model.objects, "create_user", side_effect=mock_create_user):
                    user = create_user_from_email(email)

                    self.assertIsNotNone(user)
                    self.assertEqual(user.email, email)
                    self.assertEqual(user.username, email)
                    self.assertEqual(user.custom_email, email)

                    # Verify that the custom_email field was included in the kwargs
                    # This ensures the branch where email_field != "email" is covered
                    self.assertIn("custom_email", create_user_kwargs)
                    self.assertEqual(create_user_kwargs["custom_email"], email)


class TestGetIpFromHostname(TestCase):
    """Tests for the get_ip_from_hostname function."""

    def test_get_ip_from_valid_hostname(self):
        """Test getting an IP from a valid hostname."""
        with patch("socket.getaddrinfo") as mock_getaddrinfo:
            # Mock the return value of getaddrinfo to simulate a successful lookup
            mock_getaddrinfo.return_value = [(2, 1, 6, "", ("93.184.216.34", 0))]

            ip = get_ip_from_hostname("example.com")
            self.assertEqual(ip, "93.184.216.34")
            mock_getaddrinfo.assert_called_once_with("example.com", None)

    def test_get_ip_from_ip_address(self):
        """Test getting an IP when the input is already an IP address."""
        with patch("socket.getaddrinfo") as mock_getaddrinfo:
            # Mock the return value of getaddrinfo to return the same IP
            mock_getaddrinfo.return_value = [(2, 1, 6, "", ("192.168.1.1", 0))]

            ip = get_ip_from_hostname("192.168.1.1")
            self.assertEqual(ip, "192.168.1.1")
            mock_getaddrinfo.assert_called_once_with("192.168.1.1", None)

    def test_get_ip_from_invalid_hostname(self):
        """Test getting an IP from an invalid hostname."""
        with patch("socket.getaddrinfo") as mock_getaddrinfo:
            # Mock socket.gaierror to simulate a failed lookup
            mock_getaddrinfo.side_effect = socket.gaierror("Name or service not known")

            ip = get_ip_from_hostname("invalid.hostname.that.does.not.exist")
            self.assertIsNone(ip)
            mock_getaddrinfo.assert_called_once_with("invalid.hostname.that.does.not.exist", None)

    def test_get_ip_from_empty_result(self):
        """Test getting an IP when getaddrinfo returns an empty list."""
        with patch("socket.getaddrinfo") as mock_getaddrinfo:
            # Mock the return value of getaddrinfo to return an empty list
            mock_getaddrinfo.return_value = []

            ip = get_ip_from_hostname("empty.result.com")
            self.assertIsNone(ip)
            mock_getaddrinfo.assert_called_once_with("empty.result.com", None)


class TestGetClientIp(TestCase):
    """Tests for the get_client_ip function."""

    @override_settings(SOLOMON_ANONYMIZE_IP=True)
    def test_get_client_ip_with_x_forwarded_for_valid_ip(self):
        """Test getting client IP from X-Forwarded-For header with a valid IP."""
        request = HttpRequest()
        request.META = {"HTTP_X_FORWARDED_FOR": "192.168.1.1, 10.0.0.1"}

        # Mock anonymize_ip to return an anonymized IP without calling the real function
        with patch("django_solomon.utilities.anonymize_ip", return_value="192.168.1.0") as mock_anonymize:
            ip = get_client_ip(request)
            self.assertEqual(ip, "192.168.1.0")
            mock_anonymize.assert_called_once_with("192.168.1.1")

    @override_settings(SOLOMON_ANONYMIZE_IP=True)
    def test_get_client_ip_with_x_forwarded_for_hostname(self):
        """Test getting client IP from X-Forwarded-For header with a hostname."""
        request = HttpRequest()
        request.META = {"HTTP_X_FORWARDED_FOR": "example.com, 10.0.0.1"}

        # Mock the ip_address function to raise ValueError for the hostname
        with patch("ipaddress.ip_address", side_effect=ValueError("invalid IP address")):
            # Mock get_ip_from_hostname to return a valid IP
            with patch("django_solomon.utilities.get_ip_from_hostname", return_value="93.184.216.34") as mock_get_ip:
                # Mock anonymize_ip to return an anonymized IP
                with patch("django_solomon.utilities.anonymize_ip", return_value="93.184.216.0") as mock_anonymize:
                    ip = get_client_ip(request)
                    self.assertEqual(ip, "93.184.216.0")
                    mock_get_ip.assert_called_once_with("example.com")
                    mock_anonymize.assert_called_once_with("93.184.216.34")

    @override_settings(SOLOMON_ANONYMIZE_IP=True)
    def test_get_client_ip_with_remote_addr_valid_ip(self):
        """Test getting client IP from REMOTE_ADDR with a valid IP."""
        request = HttpRequest()
        request.META = {"REMOTE_ADDR": "192.168.1.1"}

        # Mock anonymize_ip to return an anonymized IP
        with patch("django_solomon.utilities.anonymize_ip", return_value="192.168.1.0") as mock_anonymize:
            ip = get_client_ip(request)
            self.assertEqual(ip, "192.168.1.0")
            mock_anonymize.assert_called_once_with("192.168.1.1")

    @override_settings(SOLOMON_ANONYMIZE_IP=True)
    def test_get_client_ip_with_remote_addr_hostname(self):
        """Test getting client IP from REMOTE_ADDR with a hostname."""
        request = HttpRequest()
        request.META = {"REMOTE_ADDR": "example.com"}

        # Mock the ip_address function to raise ValueError for the hostname
        with patch("ipaddress.ip_address", side_effect=ValueError("invalid IP address")):
            # Mock get_ip_from_hostname to return a valid IP
            with patch("django_solomon.utilities.get_ip_from_hostname", return_value="93.184.216.34") as mock_get_ip:
                # Mock anonymize_ip to return an anonymized IP
                with patch("django_solomon.utilities.anonymize_ip", return_value="93.184.216.0") as mock_anonymize:
                    ip = get_client_ip(request)
                    self.assertEqual(ip, "93.184.216.0")
                    mock_get_ip.assert_called_once_with("example.com")
                    mock_anonymize.assert_called_once_with("93.184.216.34")

    @override_settings(SOLOMON_ANONYMIZE_IP=True)
    def test_get_client_ip_with_unresolvable_hostname(self):
        """Test getting client IP when hostname cannot be resolved."""
        request = HttpRequest()
        request.META = {"REMOTE_ADDR": "unresolvable.hostname"}

        # Mock the ip_address function to raise ValueError for the hostname
        with patch("ipaddress.ip_address", side_effect=ValueError("invalid IP address")):
            # Mock get_ip_from_hostname to return None (unresolvable)
            with patch("django_solomon.utilities.get_ip_from_hostname", return_value=None) as mock_get_ip:
                ip = get_client_ip(request)
                self.assertEqual(ip, "unresolvable.hostname")
                mock_get_ip.assert_called_once_with("unresolvable.hostname")

    @override_settings(SOLOMON_ANONYMIZE_IP=True)
    def test_get_client_ip_with_multiple_ips_in_x_forwarded_for(self):
        """Test getting client IP from X-Forwarded-For with multiple IPs."""
        request = HttpRequest()
        request.META = {"HTTP_X_FORWARDED_FOR": "192.168.1.1, 10.0.0.1, 172.16.0.1"}

        # Mock anonymize_ip to return an anonymized IP
        with patch("django_solomon.utilities.anonymize_ip", return_value="192.168.1.0") as mock_anonymize:
            ip = get_client_ip(request)
            self.assertEqual(ip, "192.168.1.0")
            mock_anonymize.assert_called_once_with("192.168.1.1")

    @override_settings(SOLOMON_ANONYMIZE_IP=False)
    def test_get_client_ip_with_anonymization_disabled(self):
        """Test getting client IP with anonymization disabled."""
        request = HttpRequest()
        request.META = {"REMOTE_ADDR": "192.168.1.1"}

        # Make sure anonymize_ip is not called
        with patch("django_solomon.utilities.anonymize_ip") as mock_anonymize:
            ip = get_client_ip(request)
            self.assertEqual(ip, "192.168.1.1")
            mock_anonymize.assert_not_called()

    @override_settings(SOLOMON_ANONYMIZE_IP=False)
    def test_get_client_ip_with_hostname_and_anonymization_disabled(self):
        """Test getting client IP from a hostname with anonymization disabled."""
        request = HttpRequest()
        request.META = {"REMOTE_ADDR": "example.com"}

        # Mock the ip_address function to raise ValueError for the hostname
        with patch("ipaddress.ip_address", side_effect=ValueError("invalid IP address")):
            # Mock get_ip_from_hostname to return a valid IP
            with patch("django_solomon.utilities.get_ip_from_hostname", return_value="93.184.216.34") as mock_get_ip:
                # Make sure anonymize_ip is not called
                with patch("django_solomon.utilities.anonymize_ip") as mock_anonymize:
                    ip = get_client_ip(request)
                    self.assertEqual(ip, "93.184.216.34")
                    mock_get_ip.assert_called_once_with("example.com")
                    mock_anonymize.assert_not_called()


class TestAnonymizeIp(TestCase):
    """Tests for the anonymize_ip function."""

    def test_anonymize_ipv4(self):
        """Test anonymizing an IPv4 address."""
        # Test with a real IPv4 address
        result = anonymize_ip("192.168.1.1")
        self.assertEqual(result, "192.168.1.0")

    def test_anonymize_ipv6(self):
        """Test anonymizing an IPv6 address."""
        # Test with a real IPv6 address
        result = anonymize_ip("2001:db8::1:2:3:4:5")
        self.assertEqual(result, "2001:db8::")

    def test_anonymize_invalid_ip(self):
        """Test anonymizing an invalid IP address."""
        # Test with an invalid IP address
        result = anonymize_ip("not-an-ip")
        self.assertEqual(result, "not-an-ip")

    def test_anonymize_other_ip_type(self):
        """Test anonymizing an IP that is neither IPv4 nor IPv6."""
        # Mock ip_address to return an object that is neither IPv4 nor IPv6
        with patch("ipaddress.ip_address") as mock_ip_address:
            mock_ip = MagicMock()
            # Make it so the object is not an instance of IPv4Address or IPv6Address
            mock_ip.__class__ = object
            mock_ip_address.return_value = mock_ip

            result = anonymize_ip("special-ip")
            self.assertEqual(result, "special-ip")
