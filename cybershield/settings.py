"""Minimal local settings for the no-database proof of concept."""

from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

# Local secrets/configuration stay on the server. The example file contains no
# secret; a real .env is ignored by Git.
load_dotenv(BASE_DIR / ".env")
AI_PROVIDER = os.environ.get("AI_PROVIDER", "openai").strip().lower()
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-6-luna").strip()

SECRET_KEY = "cybershield-local-development-key"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "assessment.apps.AssessmentConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

ROOT_URLCONF = "cybershield.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    }
]

WSGI_APPLICATION = "cybershield.wsgi.application"
ASGI_APPLICATION = "cybershield.asgi.application"

# This assessment has no models or persistence, so there is deliberately no
# configured database. Do not run migrations for this proof of concept.
DATABASES = {}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
CSRF_COOKIE_SAMESITE = "Lax"
