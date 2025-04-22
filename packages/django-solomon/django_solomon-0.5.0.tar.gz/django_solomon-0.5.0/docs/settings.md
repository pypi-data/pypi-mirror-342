---
hide:
  - navigation
---

# Settings

This guide provides detailed information about all the configurable settings in django-solomon.

## Overview

django-solomon provides several settings that you can customize in your Django settings file. These settings control
various aspects of the magic link authentication system, including link expiration, user creation, templates, and more.

## Core Settings

### SOLOMON_LINK_EXPIRATION

**Default:** `300` (seconds)

The expiration time for magic links in seconds. After this time has elapsed, the link will no longer be valid.

```python
# Set magic links to expire after 10 minutes (600 seconds)
SOLOMON_LINK_EXPIRATION = 600
```

### SOLOMON_ONLY_ONE_LINK_ALLOWED

**Default:** `True`

If enabled, only one active magic link is allowed per user. When a new magic link is requested, any existing active
links for the same user will be marked as used.

```python
# Allow multiple active magic links per user
SOLOMON_ONLY_ONE_LINK_ALLOWED = False
```

### SOLOMON_CREATE_USER_IF_NOT_FOUND

**Default:** `False`

If enabled, creates a new user when a magic link is requested for a non-existent email address.

```python
# Automatically create new users when they request a magic link
SOLOMON_CREATE_USER_IF_NOT_FOUND = True
```

### SOLOMON_LOGIN_REDIRECT_URL

**Default:** `settings.LOGIN_REDIRECT_URL`

The URL to redirect to after successful authentication with a magic link.

```python
# Redirect to the dashboard after successful authentication
SOLOMON_LOGIN_REDIRECT_URL = '/dashboard/'
```

## Permission Settings

### SOLOMON_ALLOW_ADMIN_LOGIN

**Default:** `True`

If enabled, allows superusers (admin users) to log in using magic links. If disabled, superusers will need to use the
standard Django admin login.

```python
# Disable magic link authentication for superusers
SOLOMON_ALLOW_ADMIN_LOGIN = False
```

### SOLOMON_ALLOW_STAFF_LOGIN

**Default:** `True`

If enabled, allows staff users to log in using magic links. If disabled, staff users will need to use the standard
Django admin login.

```python
# Disable magic link authentication for staff users
SOLOMON_ALLOW_STAFF_LOGIN = False
```

## IP Address Settings

django-solomon can track and validate IP addresses for enhanced security while respecting user privacy.

### SOLOMON_ENFORCE_SAME_IP

**Default:** `False`

If enabled, validates that magic links are used from the same IP address they were created from. This adds an extra
layer of security by preventing magic links from being used if intercepted by an attacker on a different network.

```python
# Enable IP validation for magic links
SOLOMON_ENFORCE_SAME_IP = True
```

### SOLOMON_ANONYMIZE_IP

**Default:** `True`

If enabled, anonymizes IP addresses before storing them. For IPv4 addresses, the last octet is removed (e.g.,
192.168.1.1 becomes 192.168.1.0). For IPv6 addresses, the last 80 bits (last 5 segments) are removed. This enhances user
privacy while still allowing for IP validation.

```python
# Disable IP anonymization (store full IP addresses)
SOLOMON_ANONYMIZE_IP = False
```

## Template Settings

django-solomon uses several templates for rendering emails and pages. You can customize these templates by providing
your own versions.

### SOLOMON_MAIL_TEXT_TEMPLATE

**Default:** `"django_solomon/email/magic_link.txt"`

The template to use for plain text magic link emails.

```python
# Use a custom plain text email template
SOLOMON_MAIL_TEXT_TEMPLATE = "myapp/emails/magic_link.txt"
```

### SOLOMON_MAIL_MJML_TEMPLATE

**Default:** `"django_solomon/email/magic_link.mjml"`

The template to use for HTML magic link emails (MJML format). django-solomon uses MJML for creating responsive HTML
emails.

```python
# Use a custom MJML email template
SOLOMON_MAIL_MJML_TEMPLATE = "myapp/emails/magic_link.mjml"
```

### SOLOMON_LOGIN_FORM_TEMPLATE

**Default:** `"django_solomon/base/login_form.html"`

The template to use for the login form page.

```python
# Use a custom login form template
SOLOMON_LOGIN_FORM_TEMPLATE = "myapp/auth/login_form.html"
```

### SOLOMON_INVALID_MAGIC_LINK_TEMPLATE

**Default:** `"django_solomon/base/invalid_magic_link.html"`

The template to use for the invalid magic link page, which is shown when a user tries to use an expired or already used
magic link.

```python
# Use a custom invalid magic link template
SOLOMON_INVALID_MAGIC_LINK_TEMPLATE = "myapp/auth/invalid_link.html"
```

### SOLOMON_MAGIC_LINK_SENT_TEMPLATE

**Default:** `"django_solomon/base/magic_link_sent.html"`

The template to use for the magic link sent confirmation page, which is shown after a user requests a magic link.

```python
# Use a custom magic link sent template
SOLOMON_MAGIC_LINK_SENT_TEMPLATE = "myapp/auth/link_sent.html"
```

## Email Settings

django-solomon uses Django's email system to send magic links. You should configure Django's email settings in your
settings file:

```python
# Example email configuration for Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

For development, you can use Django's console email backend to display emails in the console:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## Settings Summary

Here's a summary of all available settings:

| Setting                               | Default                                         | Description                                                                             |
|---------------------------------------|-------------------------------------------------|-----------------------------------------------------------------------------------------|
| `SOLOMON_LINK_EXPIRATION`             | `300`                                           | The expiration time for magic links in seconds                                          |
| `SOLOMON_ONLY_ONE_LINK_ALLOWED`       | `True`                                          | If enabled, only one active magic link is allowed per user                              |
| `SOLOMON_CREATE_USER_IF_NOT_FOUND`    | `False`                                         | If enabled, creates a new user when a magic link is requested for a non-existent email  |
| `SOLOMON_LOGIN_REDIRECT_URL`          | `settings.LOGIN_REDIRECT_URL`                   | The URL to redirect to after successful authentication                                  |
| `SOLOMON_ALLOW_ADMIN_LOGIN`           | `True`                                          | If enabled, allows superusers to log in using magic links                               |
| `SOLOMON_ALLOW_STAFF_LOGIN`           | `True`                                          | If enabled, allows staff users to log in using magic links                              |
| `SOLOMON_MAIL_TEXT_TEMPLATE`          | `"django_solomon/email/magic_link.txt"`         | The template to use for plain text magic link emails                                    |
| `SOLOMON_MAIL_MJML_TEMPLATE`          | `"django_solomon/email/magic_link.mjml"`        | The template to use for HTML magic link emails (MJML format)                            |
| `SOLOMON_LOGIN_FORM_TEMPLATE`         | `"django_solomon/base/login_form.html"`         | The template to use for the login form page                                             |
| `SOLOMON_INVALID_MAGIC_LINK_TEMPLATE` | `"django_solomon/base/invalid_magic_link.html"` | The template to use for the invalid magic link page                                     |
| `SOLOMON_MAGIC_LINK_SENT_TEMPLATE`    | `"django_solomon/base/magic_link_sent.html"`    | The template to use for the magic link sent confirmation page                           |
| `SOLOMON_ENFORCE_SAME_IP`             | `False`                                         | If enabled, validates that magic links are used from the same IP they were created from |
| `SOLOMON_ANONYMIZE_IP`                | `True`                                          | If enabled, anonymizes IP addresses before storing them                                 |
