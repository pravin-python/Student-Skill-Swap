"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application


# Base directory path
BASE_DIR = Path(__file__).resolve().parent.parent

# .environment file load karo
load_dotenv(BASE_DIR / ".environment")

os.environmentiron.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE', 'config.settings.dev'))

application = get_wsgi_application()
