from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def validate_production_settings():
    if settings.DEBUG:
        return

    if settings.SECRET_KEY == "dev-only-insecure-key":
        raise ImproperlyConfigured("DJANGO_SECRET_KEY must be set in production.")
    if "*" in settings.ALLOWED_HOSTS:
        raise ImproperlyConfigured("Wildcard ALLOWED_HOSTS is not allowed in production.")


def apply_security_settings():
    if settings.DEBUG:
        return

    settings.SECURE_SSL_REDIRECT = True
    settings.SESSION_COOKIE_SECURE = True
    settings.CSRF_COOKIE_SECURE = True
    settings.SECURE_HSTS_SECONDS = 31536000
    settings.SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    settings.SECURE_HSTS_PRELOAD = True
