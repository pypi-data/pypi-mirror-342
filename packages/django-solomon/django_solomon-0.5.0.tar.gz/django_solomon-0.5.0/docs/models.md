---
hide:
  - navigation
---

# Models and System Checks

This guide provides detailed information about the models and system checks in django-solomon.

## Models

### CustomUser

django-solomon includes a `CustomUser` model that extends Django's `AbstractUser` model to provide email-based authentication.

#### Features

- Uses email as the unique identifier for authentication instead of username
- Automatically sets the username to the email address
- Includes a custom manager (`CustomUserManager`) for creating users and superusers

#### Implementation

```python
class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)
```

#### CustomUserManager

The `CustomUserManager` provides methods for creating users and superusers with email-based authentication:

```python
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
```

### MagicLink

The `MagicLink` model is used to store magic links for authentication. It includes:

- A reference to the user
- A unique token
- Creation and expiration timestamps
- A flag to track if the link has been used
- Optional IP address tracking

### BlacklistedEmail

The `BlacklistedEmail` model is used to store email addresses that are blocked from using the magic login feature.

## System Checks

django-solomon includes system checks to ensure that your Django project is properly configured to work with the package.

### User Model Email Check

The `check_user_model_email` function checks that the user model has a unique email field, which is required for email-based authentication.

```python
@register()
def check_user_model_email(app_configs, **kwargs):
    """
    Check that the user model has a unique email field.
    """
    errors = []

    # Get the user model
    user_model = apps.get_model(settings.AUTH_USER_MODEL)

    # Check if email field exists
    try:
        email_field = user_model._meta.get_field("email")
    except Exception:
        errors.append(
            Error(
                "User model does not have an email field.",
                hint="Make sure your user model has an email field.",
                obj=settings.AUTH_USER_MODEL,
                id="django_solomon.E001",
            )
        )
        return errors

    # Check if email field is unique
    if not email_field.unique:
        errors.append(
            Error(
                "User model email field must be unique.",
                hint="Set unique=True on the email field of your user model.",
                obj=settings.AUTH_USER_MODEL,
                id="django_solomon.E002",
            )
        )

    return errors
```

This check ensures that:

1. The user model has an email field
2. The email field is set as unique

These requirements are essential for the email-based authentication that django-solomon provides.
