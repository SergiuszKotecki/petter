"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.environ.get("DJANGO_ENV") == 'prod':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.prod'
elif os.environ.get("DJANGO_ENV") == 'test':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.test')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.test'
elif os.environ.get("DJANGO_ENV") == 'dev' or os.environ.get("DJANGO_ENV") is None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.dev'

application = get_wsgi_application()
