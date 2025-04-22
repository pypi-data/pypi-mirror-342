# Changelog

All notable changes to django-solomon will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2025-04-21

### Added

- Added a custom user model that implements the `AbstractUser` model
- System check to validate that the user model has a unique email field
- Comprehensive test suite for system checks
- Improved documentation for CustomUser model
- Added documentation for system checks
- New models.md documentation file
- Updated README to mention CustomUser model and system checks

## [0.4.x] - 2025-04-20

- All versions of the 0.4.x series were yanked due to a implemention error.

## [0.3.0] - 2025-04-20

### Added

- IP address tracking for magic links
- IP validation to enhance security (optional via `SOLOMON_ENFORCE_SAME_IP` setting)
- Privacy-focused IP anonymization (enabled by default via `SOLOMON_ANONYMIZE_IP` setting)
- New utility functions for IP handling and anonymization

### Security

- Option to validate magic links are used from the same IP address they were created from
- IP anonymization to protect user privacy (removes last octet for IPv4, last 80 bits for IPv6)

## [0.2.0] - 2025-04-19

### Added

- Comprehensive guides for usage and contribution
- Parallel test execution with pytest-xdist
- Link to official documentation in README
- New badges to README
- Initial changelog structure

### Changed

- Improved documentation organization

## [0.1.3] - 2025-04-19

### Added

- Initial public release of django-solomon
- Passwordless authentication using magic links sent via email
- Configurable link expiration time (default: 300 seconds)
- Blacklist functionality to block specific email addresses
- Support for auto-creating users when they request a magic link
- Customizable templates for emails and pages
- MJML support for HTML emails
- Compatible with Django's authentication system
- Support for Django 4.2, 5.0, 5.1, and 5.2
- Support for Python 3.10, 3.11, 3.12, and 3.13
- Comprehensive test suite with high code coverage
- Full documentation

### Security

- One-time use magic links
- Option to allow only one active magic link per user
- Configurable permissions for admin and staff users
