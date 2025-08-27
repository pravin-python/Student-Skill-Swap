from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Extra dev tools
INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {name} | {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",  # INFO aur ERROR dono log karega
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/app.log",
            "formatter": "verbose",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": True,
        },
        # ORM queries ke liye
        "django.db.backends": {
            "handlers": ["file", "console"],
            "level": "DEBUG",  # Query ke liye DEBUG level
            "propagate": False,
        },
    },
}