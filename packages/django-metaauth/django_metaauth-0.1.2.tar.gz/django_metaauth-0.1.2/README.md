# Django MetaAuth

A Django app for Meta (Facebook) API authentication, providing an easy way to integrate Meta OAuth in your Django projects.

## Features

- OAuth-based authentication flow for Meta (Facebook) API
- Token storage and management
- Ready-to-use views for installation and OAuth redirection

## Installation

Install the package via pip:

```bash
pip install django-metaauth
```

## Quick Start

1. Add "metaauth" to your INSTALLED_APPS setting:

```python
INSTALLED_APPS = [
    ...
    'metaauth',
]
```

2. Include the metaauth URLconf in your project urls.py:

```python
path('meta/oauth/', include('metaauth.urls')),
```

3. Run `python manage.py migrate` to create the metaauth models.

4. Configure your Meta (Facebook) app credentials in your settings.py:

```python
METAAUTH_FACEBOOK_APP_ID = os.getenv("METAAUTH_FACEBOOK_APP_ID")
METAAUTH_FACEBOOK_APP_SECRET = os.getenv("METAAUTH_FACEBOOK_APP_SECRET")
METAAUTH_FACEBOOK_REDIRECT_URI = os.getenv("METAAUTH_FACEBOOK_REDIRECT_URI")
METAAUTH_FACEBOOK_CONFIG_ID = os.getenv("METAAUTH_FACEBOOK_CONFIG_ID")
```

5. Start the development server and visit http://127.0.0.1:8000/meta/oauth/install to begin the OAuth flow.

## Configuration

Django MetaAuth can be configured with the following settings in your Django project's settings.py file:

| Setting | Description | Default |
| ------- | ----------- | ------- |
| METAAUTH_FACEBOOK_APP_ID | Your Facebook App ID | None |
| METAAUTH_FACEBOOK_APP_SECRET | Your Facebook App Secret | None |
| METAAUTH_FACEBOOK_REDIRECT_URI | The redirect URI for OAuth | None |
| METAAUTH_FACEBOOK_API_VERSION | Facebook API version | 'v21.0' |
| METAAUTH_FACEBOOK_REQUIRED_SCOPES | Required permission scopes | ['ads_management', 'pages_show_list'] |
| METAAUTH_SUCCESS_URL | URL to redirect after successful auth | '/meta/oauth/success' |
| METAAUTH_ERROR_URL | URL to redirect after failed auth | '/meta/oauth/error' |

## Development and Testing

### Running Tests

You can run the tests without setting up a Django project:

```bash
# Run all tests
python tests.py

# Run tests with verbose output
python tests.py -v

# Run specific tests
python tests.py tests.test_models
```

### Creating Migrations

If you need to create migrations for the app:

```bash
python makemigrations.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
