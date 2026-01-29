from .base import *

DEBUG = True

ALLOWED_HOSTS= ['*']

INSTALLED_APPS +={
    "debug_toolbar",
}
MIDDLEWARE +={
    'debug_toolbar.middleware.DebugToolbarMiddleware',
}

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "db.sqlite3",
    #     "OPTIONS": {
    #         "timeout": 30,
    #     },
    # },

    "default": {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST' : os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name}: {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname}: {message}',
            'style': '{',
        },
    },

    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/admin_errors.log'),
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },

    'loggers': {
            'django.admin.customerhistory': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': False,
            },

            'django.db.backends': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
            },

            'custom': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True,
            },
        },
}