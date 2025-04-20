import logging

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mjml import mjml2html

from django_solomon.config import (
    get_login_form_template,
    get_invalid_magic_link_template,
    get_magic_link_sent_template,
    get_email_text_template,
    get_email_mjml_template,
)
from django_solomon.forms import MagicLinkForm
from django_solomon.models import BlacklistedEmail, MagicLink
from django_solomon.utilities import get_user_by_email, create_user_from_email

logger = logging.getLogger(__name__)
User = get_user_model()


def send_magic_link(request: HttpRequest) -> HttpResponse:
    """
    Handles the process of sending a magic link to a user via email. A magic link acts as a
    temporary, secure token allowing the user to authenticate without a password. The endpoint
    validates incoming requests, checks for blacklisted emails, retrieves a user based on the
    submitted email, and sends a magic link if the user exists. Supports POST and GET methods.

    Args:
        request (HttpRequest): The HTTP request object that includes metadata about the request.

    Returns:
        HttpResponse: A redirect response to the "magic_link_sent" page or renders the form template
        for sending the magic link.
    """
    if request.method == "POST":
        form = MagicLinkForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]

            # Check if the email is blacklisted
            if BlacklistedEmail.objects.filter(email=email).exists():
                logger.info(f"Blocked magic link request for blacklisted email: {email}")
                return redirect("django_solomon:magic_link_sent")

            # Get user by email
            user = get_user_by_email(email)

            # Signup unknown users if enabled in settings
            if not user and getattr(settings, "SOLOMON_CREATE_USER_IF_NOT_FOUND", False):
                user = create_user_from_email(email)

            # Send magic link if user exists
            if user:
                magic_link = MagicLink.objects.create_for_user(user)
                link_url = request.build_absolute_uri(
                    reverse(
                        "django_solomon:validate_magic_link",
                        kwargs={"token": magic_link.token},
                    )
                )
                # Calculate expiry time in minutes
                expiry_time = getattr(settings, "SOLOMON_LINK_EXPIRATION", 300) // 60  # Convert seconds to minutes

                context = {
                    "magic_link_url": link_url,
                    "expiry_time": expiry_time,
                }

                text_message = render_to_string(get_email_text_template(), context).strip()
                html_message = mjml2html(render_to_string(get_email_mjml_template(), context))

                send_mail(
                    _("Your Magic Link"),
                    text_message,
                    getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"),
                    [email],
                    fail_silently=False,
                    html_message=html_message,
                )

            return redirect("django_solomon:magic_link_sent")
    else:
        form = MagicLinkForm()
    return render(request, get_login_form_template(), {"form": form})


def magic_link_sent(request: HttpRequest) -> HttpResponse:
    """
    Renders a page that informs the user a magic link has been sent to their email.

    This view function processes an incoming HTTP request and renders the HTML page
    to indicate that the magic link email was successfully dispatched.

    Args:
        request: An HttpRequest object representing the user's request.

    Returns:
        An HttpResponse object with the rendered "magic_link_sent.html" template.
    """
    return render(request, get_magic_link_sent_template())


def validate_magic_link(request: HttpRequest, token: str) -> HttpResponse:
    """
    Validates a magic link for user authentication in a Django application. If the token is valid, the
    user is authenticated and logged in. If the token is invalid or expired, an error message is
    displayed. The function redirects authenticated users to a predetermined success URL.

    Arguments:
        request: The HTTP request object associated with the current request.
        token: A string representing the token provided in the magic link.

    Returns:
        HttpResponse: An HTTP response redirecting the user to the success URL upon successful
        authentication, or rendering an error page if authentication fails.
    """
    user = authenticate(request=request, token=token)

    if not user:
        # Get the error message from the request object, or use a default message
        error_message = getattr(request, "magic_link_error", _("Invalid or expired magic link"))

        return render(
            request,
            get_invalid_magic_link_template(),
            {"error": error_message},
        )

    # Log the user in
    login(request, user)

    # Redirect to the success URL
    success_url = getattr(settings, "SOLOMON_LOGIN_REDIRECT_URL", settings.LOGIN_REDIRECT_URL)
    return redirect(success_url)
