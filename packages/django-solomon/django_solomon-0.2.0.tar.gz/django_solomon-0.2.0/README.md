# django-solomon

[![PyPI version](https://img.shields.io/pypi/v/django-solomon.svg)](https://pypi.org/project/django-solomon/)
[![Python versions](https://img.shields.io/pypi/pyversions/django-solomon.svg)](https://pypi.org/project/django-solomon/)
[![Django versions](https://img.shields.io/pypi/djversions/django-solomon.svg)](https://pypi.org/project/django-solomon/)
[![Documentation Status](https://readthedocs.org/projects/django-solomon/badge/?version=latest)](https://django-solomon.rtfd.io/en/latest/?badge=latest)
[![Downloads](https://static.pepy.tech/badge/django-solomon)](https://pepy.tech/project/django-solomon)
[![Downloads / Month](https://pepy.tech/badge/django-solomon/month)](https://pepy.tech/project/django-solomon)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

A Django app for passwordless authentication using magic links.

## Features

- Passwordless authentication using magic links sent via email
- Configurable link expiration time
- Blacklist functionality to block specific email addresses
- Support for auto-creating users when they request a magic link
- Customizable templates for emails and pages
- Compatible with Django's authentication system

## Installation

```bash
pip install django-solomon
```

## Configuration

1. Add `django_solomon` to your `INSTALLED_APPS` in your Django settings:

```python
INSTALLED_APPS = [
    # ...
    'django_solomon',
    # ...
]
```

2. Add the authentication backend to your settings:

```python
AUTHENTICATION_BACKENDS = [
    'django_solomon.backends.MagicLinkBackend',
    'django.contrib.auth.backends.ModelBackend',  # Keep the default backend
]
```

3. Include the django-solomon URLs in your project's `urls.py`:

```python
from django.urls import include, path

urlpatterns = [
    # ...
    path('auth/', include('django_solomon.urls')),
    # ...
]
```

4. Set the login URL in your settings to use django-solomon's login view:

```python
LOGIN_URL = 'django_solomon:login'
```

This ensures that when users need to authenticate, they'll be redirected to the magic link login page.

5. Configure your email settings to ensure emails can be sent:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'your-email@example.com'
```

## Settings

django-solomon provides several settings that you can customize in your Django settings file:

| Setting                               | Default                                         | Description                                                                            |
|---------------------------------------|-------------------------------------------------|----------------------------------------------------------------------------------------|
| `SOLOMON_LINK_EXPIRATION`             | `300`                                           | The expiration time for magic links in seconds                                         |
| `SOLOMON_ONLY_ONE_LINK_ALLOWED`       | `True`                                          | If enabled, only one active magic link is allowed per user                             |
| `SOLOMON_CREATE_USER_IF_NOT_FOUND`    | `False`                                         | If enabled, creates a new user when a magic link is requested for a non-existent email |
| `SOLOMON_LOGIN_REDIRECT_URL`          | `settings.LOGIN_REDIRECT_URL`                   | The URL to redirect to after successful authentication                                 |
| `SOLOMON_ALLOW_ADMIN_LOGIN`           | `True`                                          | If enabled, allows superusers to log in using magic links                              |
| `SOLOMON_ALLOW_STAFF_LOGIN`           | `True`                                          | If enabled, allows staff users to log in using magic links                             |
| `SOLOMON_MAIL_TEXT_TEMPLATE`          | `"django_solomon/email/magic_link.txt"`         | The template to use for plain text magic link emails                                   |
| `SOLOMON_MAIL_MJML_TEMPLATE`          | `"django_solomon/email/magic_link.mjml"`        | The template to use for HTML magic link emails (MJML format)                           |
| `SOLOMON_LOGIN_FORM_TEMPLATE`         | `"django_solomon/base/login_form.html"`         | The template to use for the login form page                                            |
| `SOLOMON_INVALID_MAGIC_LINK_TEMPLATE` | `"django_solomon/base/invalid_magic_link.html"` | The template to use for the invalid magic link page                                    |
| `SOLOMON_MAGIC_LINK_SENT_TEMPLATE`    | `"django_solomon/base/magic_link_sent.html"`    | The template to use for the magic link sent confirmation page                          |

## Usage

### Basic Usage

1. Direct users to the magic link request page at `/auth/magic-link/`
2. Users enter their email address
3. A magic link is sent to their email
4. Users click the link in their email
5. They are authenticated and redirected to the success URL

### Template Customization

You can override the default templates by creating your own versions in your project:

- `django_solomon/login_form.html` - The form to request a magic link
- `django_solomon/magic_link_sent.html` - The confirmation page after a magic link is sent
- `django_solomon/invalid_magic_link.html` - The error page for invalid magic links
- `django_solomon/email/magic_link.txt` - The plain text email template for the magic link
- `django_solomon/email/magic_link.mjml` - The HTML email template for the magic link (in MJML format)

Alternatively, you can specify custom templates using the settings variables:

- `SOLOMON_LOGIN_FORM_TEMPLATE` - Custom template for the login form
- `SOLOMON_MAGIC_LINK_SENT_TEMPLATE` - Custom template for the confirmation page
- `SOLOMON_INVALID_MAGIC_LINK_TEMPLATE` - Custom template for the error page
- `SOLOMON_MAIL_TEXT_TEMPLATE` - Custom template for the plain text email
- `SOLOMON_MAIL_MJML_TEMPLATE` - Custom template for the HTML email (MJML format)

### Programmatic Usage

You can also use django-solomon programmatically in your views:

```python
from django.contrib.auth import authenticate, login
from django_solomon.models import MagicLink

# Create a magic link for a user
magic_link = MagicLink.objects.create_for_user(user)

# Authenticate a user with a token
user = authenticate(request=request, token=token)
if user:
    login(request, user)
```

## Documentation

For more detailed information, tutorials, and advanced usage examples, please visit the [official documentation](https://django-solomon.rtfd.io/).

## License

This software is licensed under [MIT license](https://codeberg.org/oliverandrich/django-solomon/src/branch/main/LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request
on [Codeberg](https://codeberg.org/oliverandrich/django-solomon).
