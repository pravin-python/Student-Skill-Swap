from .base import *
import os
import logging.config

# Initializing django getenvironment for setting debug False
DEBUG=(bool,False)

# ALLOWED_HOSTS must be configured with your domain(s).
ALLOWED_HOSTS = list(os.getenv('DJANGO_ALLOWED_HOSTS'))

# CSRF trusted origins (must match your production domain(s) with https://)
CSRF_TRUSTED_ORIGINS = list(os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS"))

# --------------------
# DATABASE CONFIGURATION
# --------------------
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", default="localhost"),
        "PORT": os.getenv("DB_PORT", default="5432"),
    }
}



# --- HTTPS SETTINGS ---
# These settings enforce HTTPS across the application.

# If your app is behind a proxy, this header tells Django it's secure.
# The tuple format is ('Header-Name', 'Header-Value')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Redirects all non-HTTPS requests to HTTPS (301 Permanent Redirect).
SECURE_SSL_REDIRECT = os.getenv('DJANGO_SECURE_SSL_REDIRECT', default=True)

# --- SECURE COOKIE SETTINGS ---

# Ensures the session cookie is only sent over HTTPS.
SESSION_COOKIE_SECURE = os.getenv('DJANGO_SESSION_COOKIE_SECURE', default=True)

# Ensures the CSRF cookie is only sent over HTTPS.
CSRF_COOKIE_SECURE = os.getenv('DJANGO_CSRF_COOKIE_SECURE', default=True)

# Prevents client-side JavaScript from accessing the CSRF cookie.
CSRF_COOKIE_HTTPONLY = True

# --- SECURITY HEADERS (via SecurityMiddleware) ---
# These headers provide browser-level security protections.

# Prevents the browser from interpreting files as a different MIME type.
SECURE_CONTENT_TYPE_NOSNIFF = os.getenv('DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)

# X-Frame-Options header to prevent clickjacking.
# Set to 'DENY' to prevent all framing of your site.
X_FRAME_OPTIONS = 'SAMEORIGIN'

# --- HTTP Strict Transport Security (HSTS) ---
# Tells the browser to always connect to your site via HTTPS for a specified period.
# This mitigates man-in-the-middle attacks.

# HSTS duration in seconds. Start with a small value (e.g., 3600 for 1 hour) for testing.
# A common production value is 31536000 (1 year).
SECURE_HSTS_SECONDS = os.getenv('DJANGO_SECURE_HSTS_SECONDS', default=2592000) # 30 days

# Apply HSTS to all subdomains.
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)

# WARNING: Only set SECURE_HSTS_PRELOAD to True if you are certain you can maintain
# HTTPS for your entire domain and all its subdomains indefinitely.
# Removal from the preload list is a very slow process.
SECURE_HSTS_PRELOAD = os.getenv('DJANGO_SECURE_HSTS_PRELOAD', default=False)

# --- CONTENT SECURITY POLICY (CSP) ---
# A powerful defense against XSS. This is a restrictive example.
# It requires careful tuning for your specific application's needs.
# For more complex policies, consider the 'django-csp' package.

# MIDDLEWARE must include 'django.middleware.csp.ContentSecurityPolicyMiddleware'
# from django.utils.csp import CSP
# SECURE_CSP = {
#     "default-src":,
#     "script-src":,  # Allows self-hosted scripts and nonced inline scripts
#     "style-src":, # Allows self-hosted and inline styles (less secure)
#     "img-src":,
#     "font-src":,
#     "object-src":,
#     "frame-ancestors":, # Redundant with X_FRAME_OPTIONS='DENY' but good practice
#     "form-action":,
#     "base-uri":,
# }

# --- FILE UPLOAD SECURITY ---

# Set secure permissions for uploaded files.
FILE_UPLOAD_PERMISSIONS = 0o640

# --------------------
# SESSION CONFIG
# --------------------
SESSION_COOKIE_AGE = 10800  # 3 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = False
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# --- LOGGING CONFIGURATION ---
# Configures logging to output structured JSON to a file for easy parsing by external services.

LOGGING_CONFIG = None
LOGLEVEL = os.getenv('DJANGO_LOGLEVEL', default='info').upper()
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(pathname)s %(lineno)d %(message)s %(context)s",
        },
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file_json": {
            "level": LOGLEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "django.log.json"),
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "json",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file_json", "console"],
            "level": LOGLEVEL,
            "propagate": True,
        },
        "django.request": {
            "handlers": ["file_json"],
            "level": "ERROR",
            "propagate": False,
        },
    },
})
    