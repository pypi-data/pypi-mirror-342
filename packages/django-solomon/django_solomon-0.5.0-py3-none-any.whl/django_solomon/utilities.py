import ipaddress
import logging
import socket

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password

logger = logging.getLogger(__name__)


def get_user_by_email(email: str) -> AbstractBaseUser | None:
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


def create_user_from_email(email: str) -> AbstractBaseUser:
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


def get_ip_from_hostname(hostname: str) -> str | None:
    try:
        addr_info = socket.getaddrinfo(hostname, None)
        if addr_info:
            return addr_info[0][4][0]
        return None
    except socket.gaierror:
        return None


def anonymize_ip(ip_str: str) -> str:
    """
    Anonymize an IP address by removing the last octet for IPv4 or
    the last 80 bits (last 5 segments) for IPv6.

    Args:
        ip_str: The IP address to anonymize.

    Returns:
        The anonymized IP address.
    """
    try:
        ip = ipaddress.ip_address(ip_str)

        if isinstance(ip, ipaddress.IPv4Address):
            # For IPv4, zero out the last octet
            # Convert to integer, mask with 0xFFFFFF00 to zero last octet, convert back
            masked_ip = ipaddress.IPv4Address(int(ip) & 0xFFFFFF00)
            return str(masked_ip)
        elif isinstance(ip, ipaddress.IPv6Address):
            # For IPv6, zero out the last 80 bits (last 5 segments)
            # Convert to integer, mask with ~(2^80-1) to zero last 80 bits, convert back
            masked_ip = ipaddress.IPv6Address(int(ip) & ~((1 << 80) - 1))
            return str(masked_ip)
        return ip_str
    except ValueError:
        # If it's not a valid IP address, return as is
        return ip_str


def get_client_ip(request) -> str:
    # Check X-Forwarded-For header first
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")

    # Check if the value is a valid IP address
    try:
        ipaddress.ip_address(ip)
        # Anonymize IP if the setting is enabled (default is True)
        if getattr(settings, "SOLOMON_ANONYMIZE_IP", True):
            return anonymize_ip(ip)
        return ip
    except ValueError:
        # Not a valid IP, try to resolve as hostname
        resolved_ip = get_ip_from_hostname(ip)
        if resolved_ip:
            # Anonymize the resolved IP if the setting is enabled
            if getattr(settings, "SOLOMON_ANONYMIZE_IP", True):
                return anonymize_ip(resolved_ip)
            return resolved_ip
        return ip
