# Django Google Ads Authentication

A Django app that provides Google Ads API authentication and basic functionality for managing campaigns.

## Features

- OAuth2 authentication with Google Ads API
- Store and manage refresh tokens
- Track campaign statuses
- Basic campaign management functionality

## Installation

Install the package using pip:

```bash
pip install django-googleadsauth
```
## local installation
1. clone the repo
2. add a volume in your docker compose setup pointing to the package directory
```shell
    volumes:
      - ./app/src:/app/src
      - ./app/logs:/app/logs
      - ./app/logs/gunicorn:/var/log/gunicorn
      - ./app/local-cdn:/app/local-cdn
      - /home/tarik/django-googleadsauth:/app/django-googleadsauth
```
3. in your `pyproject.toml` add a dependency
```shell

dependencies = [
    "django>=5.1.5",
    ...
    "django-googleadsauth @ file:///app/django-googleadsauth"
]
```
4. make sure to freeze the dependencies in the `requirements.txt file`
```shell
uv pip compile pyproject.toml -o requirements.txt 
```

## Configuration

1. Add `googleadsauth` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'googleadsauth',
    ...
]
```
2. configure your `.env` file
```dotenv
GOOGLE_ADS_CLIENT_SECRET_PATH=/app/google-secret.json
GOOGLE_ADS_REDIRECT_URI=http://localhost:8082/google/oauth/redirect
GOOGLE_ADS_DEVELOPER_TOKEN=xxxxxxxx
GOOGLE_ADS_CLIENT_ID=xxxxx
GOOGLE_ADS_CLIENT_SECRET=xxxx
GOOGLE_ADS_TOKEN_URI=https://oauth2.googleapis.com/token
GOOGLE_ADS_MANAGER_ACCOUNT_ID=xxxx
```

2. Add the required Google Ads API settings to your `settings.py`:

```python
GOOGLE_ADS = {
    'CLIENT_SECRET_PATH': os.getenv('GOOGLE_ADS_CLIENT_SECRET_PATH'),
    'REDIRECT_URI': os.getenv('GOOGLE_ADS_REDIRECT_URI'),
    'DEVELOPER_TOKEN': os.getenv('GOOGLE_ADS_DEVELOPER_TOKEN'),
    'CLIENT_ID': os.getenv('GOOGLE_ADS_CLIENT_ID'),
    'CLIENT_SECRET': os.getenv('GOOGLE_ADS_CLIENT_SECRET'),
    'MANAGER_ACCOUNT_ID': os.getenv('GOOGLE_ADS_MANAGER_ACCOUNT_ID'),  # Optional
}
```

3. Include the app URLs in your project's `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path('googleads/', include('googleadsauth.urls')),
    ...
]
```

4. Run migrations:

```bash
python manage.py migrate googleadsauth
```

## Usage

### Authentication

1. Navigate to `/googleads/auth/` to start the OAuth2 authentication flow
2. After successful authentication, the app will store the refresh token


## Development

To set up for development:

1. Clone the repository
2. Install development dependencies
3. Run the test suite

## License

MIT License
