---
hide:
  - navigation
---

# Installation and Setup

This guide will walk you through the process of installing and setting up django-solomon in your Django project.

## Prerequisites

Before installing django-solomon, ensure you have:

- Python 3.10 or higher
- Django 4.2 or higher
- A working email configuration for sending magic links

## Installation Methods

### Using pip (Recommended)

The simplest way to install django-solomon is using pip:

```bash
pip install django-solomon
```

### Using a Virtual Environment

It's recommended to install django-solomon in a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install django-solomon
pip install django-solomon
```

### From Source

You can also install django-solomon directly from the source code:

```bash
git clone https://codeberg.org/oliverandrich/django-solomon.git
cd django-solomon
pip install -e .
```

## Configuration Steps

After installing django-solomon, you need to configure your Django project to use it:

### 1. Add to INSTALLED_APPS

Add `django_solomon` to your `INSTALLED_APPS` in your Django settings:

```python
INSTALLED_APPS = [
    # ...
    'django_solomon',
    # ...
]
```

### 2. Configure Authentication Backend

Add the authentication backend to your settings:

```python
AUTHENTICATION_BACKENDS = [
    'django_solomon.backends.MagicLinkBackend',
    'django.contrib.auth.backends.ModelBackend',  # Keep the default backend
]
```

### 3. Include URLs

Include the django-solomon URLs in your project's `urls.py`:

```python
from django.urls import include, path

urlpatterns = [
    # ...
    path('auth/', include('django_solomon.urls')),
    # ...
]
```

### 4. Set Login URL

Set the login URL in your settings to use django-solomon's login view:

```python
LOGIN_URL = 'django_solomon:login'
```

This ensures that when users need to authenticate, they'll be redirected to the magic link login page.

### 5. Configure Email Settings

Configure your email settings to ensure magic link emails can be sent:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'your-email@example.com'
```

For development, you can use Django's console email backend to display emails in the console:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## Customizing Settings

django-solomon provides several settings that you can customize in your Django settings file. For a comprehensive list of all available settings and their detailed descriptions, please refer to the [Settings documentation](settings.md).

## Verifying Installation

To verify that django-solomon is correctly installed and configured:

1. Start your Django development server:
   ```bash
   python manage.py runserver
   ```

2. Navigate to the login URL (e.g., `http://localhost:8000/auth/magic-link/`)

3. Enter an email address and request a magic link

4. Check that the magic link is sent (in the console if using the console email backend)

5. Click the magic link to authenticate

## Troubleshooting

### Magic Links Not Being Sent

- Check your email configuration settings
- Ensure your SMTP server is accessible
- Try using the console email backend for testing

### Authentication Not Working

- Verify that the MagicLinkBackend is in your AUTHENTICATION_BACKENDS
- Check that the URLs are correctly included in your urls.py
- Ensure the magic link hasn't expired or been used already

### Template Errors

- Make sure django_solomon is in your INSTALLED_APPS
- Check that you're not overriding templates incorrectly
- Verify that your custom templates extend the correct base templates

## Next Steps

Now that you have django-solomon installed and configured, you can:

- Customize the templates to match your site's design
- Integrate the magic link login with your existing authentication flow
- Explore the programmatic API for advanced usage
