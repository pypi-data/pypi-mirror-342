from django.conf import settings


def get_email_text_template():
    return getattr(settings, "SOLOMON_MAIL_TEXT_TEMPLATE", None) or "django_solomon/email/magic_link.txt"


def get_email_mjml_template():
    return getattr(settings, "SOLOMON_MAIL_MJML_TEMPLATE", None) or "django_solomon/email/magic_link.mjml"


def get_login_form_template():
    return getattr(settings, "SOLOMON_LOGIN_FORM_TEMPLATE", None) or "django_solomon/base/login_form.html"


def get_invalid_magic_link_template():
    return (
        getattr(settings, "SOLOMON_INVALID_MAGIC_LINK_TEMPLATE", None) or "django_solomon/base/invalid_magic_link.html"
    )


def get_magic_link_sent_template():
    return getattr(settings, "SOLOMON_MAGIC_LINK_SENT_TEMPLATE", None) or "django_solomon/base/magic_link_sent.html"
