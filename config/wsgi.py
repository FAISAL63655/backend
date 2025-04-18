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
if hasattr(settings, 'MEDIA_ROOT') and settings.MEDIA_ROOT:
    # Asegurarse de que el prefijo no tenga barras iniciales para WhiteNoise
    media_prefix = settings.MEDIA_URL
    if media_prefix.startswith('/'):
        media_prefix = media_prefix[1:]

    print(f"Adding media files from {settings.MEDIA_ROOT} with prefix {media_prefix}")
    application.add_files(settings.MEDIA_ROOT, prefix=media_prefix)
