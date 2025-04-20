import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from django_solomon.models import UserType

logger = logging.getLogger(__name__)


def get_user_by_email(email: str) -> UserType | None:
    """
    Get a user by email.

    This method supports both the standard User model and custom User models
    by checking if the email field exists on the model.

    Args:
        email: The email to look up.

    Returns:
        The user if found, None otherwise.
    """
    user_model = get_user_model()

    # Check if the user model has an email field
    if hasattr(user_model, "EMAIL_FIELD"):
        email_field = user_model.EMAIL_FIELD
    else:
        email_field = "email"

    # Make sure the email field exists on the model
    if not hasattr(user_model, email_field):
        logger.warning(f"User model {user_model.__name__} does not have field {email_field}, falling back to 'email'")
        email_field = "email"

        # Check if the fallback field exists
        if not hasattr(user_model, email_field):
            logger.error(f"User model {user_model.__name__} does not have an email field")
            return None

    # Query for the user
    try:
        query = {email_field: email}
        return user_model.objects.get(**query)
    except user_model.DoesNotExist:
        return None
    except Exception as e:
        logger.error(f"Error getting user by email: {e}")
        return None


def create_user_from_email(email: str) -> UserType:
    """
    Creates a new user with the given email.

    This function uses the email as both the username and email address
    for the new user.

    Args:
        email: The email to use for the new user.

    Returns:
        The newly created user.
    """
    user_model = get_user_model()

    # Create the user with email as username
    user_kwargs = {
        "username": email,
        "email": email,
        "password": make_password(None),
    }

    # Check if the user model has an email field
    if hasattr(user_model, "EMAIL_FIELD"):
        email_field = user_model.EMAIL_FIELD
        if email_field != "email":
            user_kwargs[email_field] = email

    return user_model.objects.create_user(**user_kwargs)
