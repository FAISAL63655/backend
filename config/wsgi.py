"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Configurar la aplicación WSGI
application = get_wsgi_application()

# Usar WhiteNoise para servir archivos estáticos y media
application = WhiteNoise(application)

# Configurar WhiteNoise para servir archivos estáticos
application.add_files(settings.STATIC_ROOT, prefix=settings.STATIC_URL)

# Agregar soporte para servir archivos de medios
if hasattr(settings, 'MEDIA_ROOT') and settings.MEDIA_ROOT:
    # Asegurarse de que el prefijo no tenga barras iniciales para WhiteNoise
    media_prefix = settings.MEDIA_URL
    if media_prefix.startswith('/'):
        media_prefix = media_prefix[1:]

    # Imprimir información de depuración
    print(f"\n\n=== MEDIA CONFIGURATION ===")
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    print(f"Using prefix for WhiteNoise: {media_prefix}")

    # Verificar si el directorio existe
    if os.path.exists(settings.MEDIA_ROOT):
        print(f"Media directory exists: {settings.MEDIA_ROOT}")
        # Listar archivos en el directorio
        try:
            files = os.listdir(settings.MEDIA_ROOT)
            print(f"Files in media directory: {files}")

            # Verificar subdirectorio students
            students_dir = os.path.join(settings.MEDIA_ROOT, 'students')
            if os.path.exists(students_dir):
                print(f"Students directory exists: {students_dir}")
                student_files = os.listdir(students_dir)
                print(f"Files in students directory: {student_files}")
            else:
                print(f"Students directory does not exist: {students_dir}")
                # Crear el directorio si no existe
                os.makedirs(students_dir, exist_ok=True)
                print(f"Created students directory: {students_dir}")
        except Exception as e:
            print(f"Error listing files: {e}")
    else:
        print(f"Media directory does not exist: {settings.MEDIA_ROOT}")
        # Crear el directorio si no existe
        try:
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'students'), exist_ok=True)
            print(f"Created media directories: {settings.MEDIA_ROOT}")
        except Exception as e:
            print(f"Error creating directories: {e}")

    # Agregar archivos de media a WhiteNoise
    try:
        application.add_files(settings.MEDIA_ROOT, prefix=media_prefix)
        print(f"Successfully added media files to WhiteNoise")
    except Exception as e:
        print(f"Error adding media files to WhiteNoise: {e}")
        # Imprimir información del sistema para depuración
        print(f"Python version: {sys.version}")
        print(f"WhiteNoise version: {WhiteNoise.__version__}")

    print("=== END MEDIA CONFIGURATION ===\n\n")
