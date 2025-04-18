#!/usr/bin/env python
"""
Script para verificar y corregir los permisos de los archivos de medios.
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def fix_permissions():
    """Verificar y corregir los permisos de los archivos de medios."""
    print("\n=== MEDIA PERMISSIONS FIX ===")
    
    # Verificar si MEDIA_ROOT está configurado
    if not hasattr(settings, 'MEDIA_ROOT') or not settings.MEDIA_ROOT:
        print("MEDIA_ROOT no está configurado.")
        return
    
    media_root = settings.MEDIA_ROOT
    print(f"MEDIA_ROOT: {media_root}")
    
    # Verificar si el directorio existe
    if not os.path.exists(media_root):
        print(f"El directorio MEDIA_ROOT no existe: {media_root}")
        try:
            os.makedirs(media_root, exist_ok=True)
            print(f"Directorio MEDIA_ROOT creado: {media_root}")
        except Exception as e:
            print(f"Error al crear el directorio MEDIA_ROOT: {e}")
            return
    
    # Establecer permisos para MEDIA_ROOT
    try:
        os.chmod(media_root, 0o755)
        print(f"Permisos establecidos para MEDIA_ROOT: 755")
    except Exception as e:
        print(f"Error al establecer permisos para MEDIA_ROOT: {e}")
    
    # Verificar subdirectorios
    for root, dirs, files in os.walk(media_root):
        # Establecer permisos para directorios
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                os.chmod(dir_path, 0o755)
                print(f"Permisos establecidos para directorio: {dir_path}")
            except Exception as e:
                print(f"Error al establecer permisos para directorio {dir_path}: {e}")
        
        # Establecer permisos para archivos
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                os.chmod(file_path, 0o644)
                print(f"Permisos establecidos para archivo: {file_path}")
            except Exception as e:
                print(f"Error al establecer permisos para archivo {file_path}: {e}")
    
    print("=== MEDIA PERMISSIONS FIX COMPLETED ===\n")

if __name__ == "__main__":
    fix_permissions()
