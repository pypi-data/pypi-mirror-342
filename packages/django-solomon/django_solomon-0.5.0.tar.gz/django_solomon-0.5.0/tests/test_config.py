from django.test import override_settings, SimpleTestCase

from django_solomon.config import (
    get_email_text_template,
    get_email_mjml_template,
    get_login_form_template,
    get_invalid_magic_link_template,
    get_magic_link_sent_template,
)


class TestConfig(SimpleTestCase):
    """Tests for the config module."""

    def test_get_email_text_template_default(self):
        """Test that get_email_text_template returns the default template when the setting is not defined."""
        assert get_email_text_template() == "django_solomon/email/magic_link.txt"

    @override_settings(SOLOMON_MAIL_TEXT_TEMPLATE="custom/email_template.txt")
    def test_get_email_text_template_custom(self):
        """Test that get_email_text_template returns the custom template when the setting is defined."""
        assert get_email_text_template() == "custom/email_template.txt"

    @override_settings(SOLOMON_MAIL_TEXT_TEMPLATE=None)
    def test_get_email_text_template_none(self):
        """Test that get_email_text_template returns the default template when the setting is explicitly None."""
        assert get_email_text_template() == "django_solomon/email/magic_link.txt"

    def test_get_email_mjml_template_default(self):
        """Test that get_email_mjml_template returns the default template when the setting is not defined."""
        assert get_email_mjml_template() == "django_solomon/email/magic_link.mjml"

    @override_settings(SOLOMON_MAIL_MJML_TEMPLATE="custom/email_template.mjml")
    def test_get_email_mjml_template_custom(self):
        """Test that get_email_mjml_template returns the custom template when the setting is defined."""
        assert get_email_mjml_template() == "custom/email_template.mjml"

    @override_settings(SOLOMON_MAIL_MJML_TEMPLATE=None)
    def test_get_email_mjml_template_none(self):
        """Test that get_email_mjml_template returns the default template when the setting is explicitly None."""
        assert get_email_mjml_template() == "django_solomon/email/magic_link.mjml"

    def test_get_login_form_template_default(self):
        """Test that get_login_form_template returns the default template when the setting is not defined."""
        assert get_login_form_template() == "django_solomon/base/login_form.html"

    @override_settings(SOLOMON_LOGIN_FORM_TEMPLATE="custom/login_form.html")
    def test_get_login_form_template_custom(self):
        """Test that get_login_form_template returns the custom template when the setting is defined."""
        assert get_login_form_template() == "custom/login_form.html"

    @override_settings(SOLOMON_LOGIN_FORM_TEMPLATE=None)
    def test_get_login_form_template_none(self):
        """Test that get_login_form_template returns the default template when the setting is explicitly None."""
        assert get_login_form_template() == "django_solomon/base/login_form.html"

    def test_get_invalid_magic_link_template_default(self):
        """Test that get_invalid_magic_link_template returns the default template when the setting is not defined."""
        assert get_invalid_magic_link_template() == "django_solomon/base/invalid_magic_link.html"

    @override_settings(SOLOMON_INVALID_MAGIC_LINK_TEMPLATE="custom/invalid_magic_link.html")
    def test_get_invalid_magic_link_template_custom(self):
        """Test that get_invalid_magic_link_template returns the custom template when the setting is defined."""
        assert get_invalid_magic_link_template() == "custom/invalid_magic_link.html"

    @override_settings(SOLOMON_INVALID_MAGIC_LINK_TEMPLATE=None)
    def test_get_invalid_magic_link_template_none(self):
        """Test that get_invalid_magic_link_template returns the default template when the setting is explicitly None"""
        assert get_invalid_magic_link_template() == "django_solomon/base/invalid_magic_link.html"

    def test_get_magic_link_sent_template_default(self):
        """Test that get_magic_link_sent_template returns the default template when the setting is not defined."""
        assert get_magic_link_sent_template() == "django_solomon/base/magic_link_sent.html"

    @override_settings(SOLOMON_MAGIC_LINK_SENT_TEMPLATE="custom/magic_link_sent.html")
    def test_get_magic_link_sent_template_custom(self):
        """Test that get_magic_link_sent_template returns the custom template when the setting is defined."""
        assert get_magic_link_sent_template() == "custom/magic_link_sent.html"

    @override_settings(SOLOMON_MAGIC_LINK_SENT_TEMPLATE=None)
    def test_get_magic_link_sent_template_none(self):
        """Test that get_magic_link_sent_template returns the default template when the setting is explicitly None."""
        assert get_magic_link_sent_template() == "django_solomon/base/magic_link_sent.html"
