"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# Usar WhiteNoise para servir archivos estáticos
application = WhiteNoise(application)

# Agregar soporte para servir archivos de medios en producción
if not settings.DEBUG and hasattr(settings, 'MEDIA_ROOT') and settings.MEDIA_ROOT:
    application.add_files(settings.MEDIA_ROOT, prefix=settings.MEDIA_URL)
