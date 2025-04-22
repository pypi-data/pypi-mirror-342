from unittest.mock import patch, Mock

from django.core.checks import Error
from django.test import SimpleTestCase

from django_solomon.checks import check_user_model_email


class TestSystemChecks(SimpleTestCase):
    """Tests for the system checks."""

    def test_check_user_model_email_success(self):
        """Test that the check passes when the user model has a unique email field."""
        # The default test settings use CustomUser which has a unique email field
        errors = check_user_model_email(None)
        self.assertEqual(errors, [])

    @patch("django_solomon.checks.apps.get_model")
    def test_check_user_model_email_missing(self, mock_get_model):
        """Test that the check fails when the user model doesn't have an email field."""
        # Mock a user model without an email field
        mock_user_model = Mock()
        mock_user_model._meta.get_field.side_effect = Exception("Field does not exist")
        mock_get_model.return_value = mock_user_model

        errors = check_user_model_email(None)

        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], Error)
        self.assertEqual(errors[0].id, "django_solomon.E001")
        self.assertEqual(errors[0].msg, "User model does not have an email field.")

    @patch("django_solomon.checks.apps.get_model")
    def test_check_user_model_email_not_unique(self, mock_get_model):
        """Test that the check fails when the user model's email field is not unique."""
        # Mock a user model with a non-unique email field
        mock_user_model = Mock()
        mock_email_field = Mock()
        mock_email_field.unique = False
        mock_user_model._meta.get_field.return_value = mock_email_field
        mock_get_model.return_value = mock_user_model

        errors = check_user_model_email(None)

        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], Error)
        self.assertEqual(errors[0].id, "django_solomon.E002")
        self.assertEqual(errors[0].msg, "User model email field must be unique.")
