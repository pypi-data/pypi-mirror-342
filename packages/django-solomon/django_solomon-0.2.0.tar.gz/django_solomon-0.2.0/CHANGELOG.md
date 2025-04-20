# Changelog

All notable changes to django-solomon will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
