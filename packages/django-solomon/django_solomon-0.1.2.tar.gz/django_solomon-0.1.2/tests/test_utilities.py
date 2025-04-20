from unittest.mock import patch, MagicMock

import pytest
from django.contrib.auth import get_user_model

from django_solomon.utilities import get_user_by_email, create_user_from_email


@pytest.mark.django_db
class TestGetUserByEmail:
    """Tests for the get_user_by_email function."""

    def test_get_user_by_email_with_existing_user(self, user):
        """Test getting a user by email when the user exists."""
        # The user fixture creates a user with email "test@example.com"
        found_user = get_user_by_email("test@example.com")
        assert found_user is not None
        assert found_user.email == "test@example.com"
        assert found_user.username == "testuser"

    def test_get_user_by_email_with_nonexistent_email(self):
        """Test getting a user by email when the email doesn't exist."""
        found_user = get_user_by_email("nonexistent@example.com")
        assert found_user is None

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
                    assert found_user is not None
                    assert found_user.custom_email == "custom@example.com"

    def test_get_user_by_email_with_no_email_field(self):
        """Test getting a user by email when the user model doesn't have an email field."""
        # Mock hasattr to return False for both EMAIL_FIELD and 'email'
        with patch("django_solomon.utilities.hasattr", return_value=False):
            found_user = get_user_by_email("test@example.com")
            assert found_user is None

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
                assert found_user is None
                # Verify that hasattr was called 3 times
                assert call_count == 3

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
                assert found_user is None

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
                    assert found_user is not None
                    assert found_user.email == "test@example.com"
                    # Verify that hasattr was called 3 times
                    assert call_count == 3

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
                assert found_user is not None
                assert found_user.email == "test@example.com"

    def test_get_user_by_email_with_exception(self):
        """Test getting a user by email when an exception occurs."""
        User = get_user_model()

        # Mock User.objects.get to raise an exception
        with patch.object(User.objects, "get", side_effect=Exception("Test exception")):
            found_user = get_user_by_email("test@example.com")
            assert found_user is None

    def test_get_user_by_email_with_does_not_exist_exception(self):
        """Test getting a user by email when DoesNotExist exception occurs."""
        # This is already tested in test_get_user_by_email_with_nonexistent_email
        # but we'll test it explicitly here for completeness
        found_user = get_user_by_email("nonexistent@example.com")
        assert found_user is None


@pytest.mark.django_db
class TestCreateUserFromEmail:
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

                assert user is not None
                assert user.email == email
                assert user.username == email

                # Verify that only the standard fields were included in the kwargs
                assert "username" in create_user_kwargs
                assert "email" in create_user_kwargs
                assert "password" in create_user_kwargs
                assert len(create_user_kwargs) == 3  # Only these three fields

    def test_create_user_from_email_standard(self):
        """Test creating a user with a standard email."""
        email = "newuser@example.com"
        user = create_user_from_email(email)

        assert user is not None
        assert user.email == email
        assert user.username == email

        # Verify the user was actually created in the database
        User = get_user_model()
        db_user = User.objects.get(email=email)
        assert db_user is not None
        assert db_user.email == email
        assert db_user.username == email

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

                    assert user is not None
                    assert user.email == email
                    assert user.username == email

                    # Verify that only the standard fields were included in the kwargs
                    # This ensures the branch where email_field == "email" is covered
                    assert "username" in create_user_kwargs
                    assert "email" in create_user_kwargs
                    assert "password" in create_user_kwargs
                    assert len(create_user_kwargs) == 3  # Only these three fields

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

                    assert user is not None
                    assert user.email == email
                    assert user.username == email
                    assert user.custom_email == email

                    # Verify that the custom_email field was included in the kwargs
                    # This ensures the branch where email_field != "email" is covered
                    assert "custom_email" in create_user_kwargs
                    assert create_user_kwargs["custom_email"] == email
