---
hide:
  - navigation
---

# Templates

This guide provides detailed information about all the templates used in django-solomon and the context variables
available in each template.

## Overview

django-solomon uses several templates for rendering emails and pages. You can customize these templates by providing
your own versions or by specifying custom templates using the settings variables.

## HTML Templates

### Login Form Template

**Default Path:** `django_solomon/base/login_form.html`

**Settings Variable:** `SOLOMON_LOGIN_FORM_TEMPLATE`

**Description:** This template renders the form for requesting a magic link.

**Context Variables:**

- `form`: The MagicLinkForm instance that contains the email field.

**Example Usage:**

```html
{% extends "base.html" %}
{% load i18n %}

{% block title %}{% translate "Magic Link Login" %}{% endblock %}

{% block content %}
<div class="container">
    <h1>{% translate "Magic Link Login" %}</h1>
    <p>{% translate "Enter your email address to receive a magic link for logging in." %}</p>

    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">{% translate "Send Magic Link" %}</button>
    </form>
</div>
{% endblock content %}
```

### Magic Link Sent Template

**Default Path:** `django_solomon/base/magic_link_sent.html`

**Settings Variable:** `SOLOMON_MAGIC_LINK_SENT_TEMPLATE`

**Description:** This template is displayed after a user requests a magic link, confirming that the link has been sent.

**Context Variables:**

- No specific context variables are passed to this template.

**Example Usage:**

```html
{% extends "base.html" %}
{% load i18n %}

{% block title %}{% translate "Magic Link Sent" %}{% endblock %}

{% block content %}
<div class="container">
    <h1>{% translate "Magic Link Sent" %}</h1>
    <p>{% translate "If an account exists with the email address you provided, we've sent a magic link to that address."
        %}</p>
    <p>{% translate "Please check your email and click the link to log in." %}</p>
</div>
{% endblock content %}
```

### Invalid Magic Link Template

**Default Path:** `django_solomon/base/invalid_magic_link.html`

**Settings Variable:** `SOLOMON_INVALID_MAGIC_LINK_TEMPLATE`

**Description:** This template is displayed when a user clicks on an invalid or expired magic link.

**Context Variables:**

- `error`: A string containing the error message explaining why the magic link is invalid.

**Example Usage:**

```html
{% extends "base.html" %}
{% load i18n %}

{% block title %}{% translate "Invalid Magic Link" %}{% endblock %}

{% block content %}
<div class="container">
    <h1>{% translate "Invalid Magic Link" %}</h1>
    <p>{{ error }}</p>
    <p>{% translate "Please request a new magic link to log in." %}</p>

    <a href="{% url 'django_solomon:login' %}" class="btn btn-primary">
        {% translate "Request New Magic Link" %}
    </a>
</div>
{% endblock content %}
```

## Email Templates

django-solomon uses two types of email templates: a plain text template and an MJML template for HTML emails.

### Plain Text Email Template

**Default Path:** `django_solomon/email/magic_link.txt`

**Settings Variable:** `SOLOMON_MAIL_TEXT_TEMPLATE`

**Description:** This template is used to generate the plain text version of the magic link email.

**Context Variables:**

- `magic_link_url`: The absolute URL of the magic link that the user needs to click.
- `expiry_time`: The expiration time of the magic link in minutes.

**Example Usage:**

```
{% load i18n %}
{% translate "Hello," %}

{% translate "You requested a magic link to log in to your account. Please click the link below to log in:" %}

{{ magic_link_url }}

{% blocktranslate with expiry_time=expiry_time %}This link will expire in {{ expiry_time }} minutes. If you did not request this link, you can safely ignore this email.{% endblocktranslate %}

{% translate "Thank you," %}
{% translate "The Django Solomon Team" %}

---
{% translate "This email was sent by Django Solomon." %}
```

### MJML Email Template

**Default Path:** `django_solomon/email/magic_link.mjml`

**Settings Variable:** `SOLOMON_MAIL_MJML_TEMPLATE`

**Description:** This template is used to generate the HTML version of the magic link email using MJML, which ensures
responsive emails across different email clients. For more information about MJML syntax and components, see the [MJML documentation](https://mjml.io/documentation/).

**Context Variables:**

- `magic_link_url`: The absolute URL of the magic link that the user needs to click.
- `expiry_time`: The expiration time of the magic link in minutes.

**Example Usage:**

```html
{% load i18n %}
<mjml>
    <mj-body>
        <mj-section>
            <mj-column>
                <mj-text>
                    <p>{% translate "Hello," %}</p>

                    <p>
                        {% blocktranslate %}
                        You requested a magic link to log in to your account. Please click the link below
                        to log in:
                        {% endblocktranslate %}
                    </p>
                </mj-text>

                <mj-button href="{{ magic_link_url }}">{% translate "Click here to log in" %}</mj-button>

                <mj-text>
                    <p>
                        {% blocktranslate with expiry_time=expiry_time %}
                        This link will expire in {{ expiry_time }} minutes. If you did not
                        request this link, you can safely ignore this email.
                        {% endblocktranslate %}
                    </p>

                    <p>
                        {% translate "Thank you," %}
                        <br>
                        {% translate "The Django Solomon Team" %}
                    </p>

                    <p>
                        ---
                        <br>
                        {% translate "This email was sent by Django Solomon." %}
                    </p>
                </mj-text>
            </mj-column>
        </mj-section>
    </mj-body>
</mjml>
```

## Customizing Templates

You can customize the templates in two ways:

1. **Override the default templates**: Create your own templates with the same paths in your project's templates
   directory.

2. **Specify custom templates in settings**: Use the settings variables to specify the paths to your custom templates.

### Example: Overriding the Default Templates

Create the following directory structure in your project:

```
templates/
└── django_solomon/
    ├── base/
    │   ├── login_form.html
    │   ├── magic_link_sent.html
    │   └── invalid_magic_link.html
    └── email/
        ├── magic_link.txt
        └── magic_link.mjml
```

### Example: Specifying Custom Templates in Settings

```python
# In your settings.py file
SOLOMON_LOGIN_FORM_TEMPLATE = "myapp/auth/login_form.html"
SOLOMON_MAGIC_LINK_SENT_TEMPLATE = "myapp/auth/link_sent.html"
SOLOMON_INVALID_MAGIC_LINK_TEMPLATE = "myapp/auth/invalid_link.html"
SOLOMON_MAIL_TEXT_TEMPLATE = "myapp/emails/magic_link.txt"
SOLOMON_MAIL_MJML_TEMPLATE = "myapp/emails/magic_link.mjml"
```

## Base Template Requirements

All the HTML templates extend a `base.html` template, which should be provided by your project. The base template should
define at least the following blocks:

- `title`: Used for the page title
- `content`: Used for the main content of the page

If your base template uses different block names, you'll need to modify the django-solomon templates accordingly.
