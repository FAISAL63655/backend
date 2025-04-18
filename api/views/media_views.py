"""
Vistas para servir archivos de medios.
"""

import os
import mimetypes
from django.http import HttpResponse, Http404
from django.conf import settings
from django.views.decorators.cache import cache_control

@cache_control(max_age=86400)  # Cache por 24 horas
def serve_media_file(request, path):
    """
    Sirve un archivo de medios directamente.
    
    Args:
        request: La solicitud HTTP.
        path: La ruta del archivo dentro del directorio de medios.
    
    Returns:
        HttpResponse con el contenido del archivo.
    
    Raises:
        Http404: Si el archivo no existe.
    """
    # Construir la ruta completa del archivo
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    # Verificar si el archivo existe
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        # Registrar información de depuración
        print(f"Archivo no encontrado: {file_path}")
        print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
        print(f"Path solicitado: {path}")
        
        # Listar archivos en el directorio de medios
        try:
            media_files = []
            for root, dirs, files in os.walk(settings.MEDIA_ROOT):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), settings.MEDIA_ROOT)
                    media_files.append(rel_path)
            print(f"Archivos disponibles en MEDIA_ROOT: {media_files}")
        except Exception as e:
            print(f"Error al listar archivos: {e}")
        
        raise Http404(f"Archivo no encontrado: {path}")
    
    # Determinar el tipo MIME del archivo
    content_type, encoding = mimetypes.guess_type(file_path)
    content_type = content_type or 'application/octet-stream'
    
    # Leer el archivo
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Crear la respuesta
        response = HttpResponse(file_content, content_type=content_type)
        
        # Establecer encabezados adicionales
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
        if encoding:
            response['Content-Encoding'] = encoding
        
        # Establecer encabezados de caché
        response['Cache-Control'] = 'public, max-age=86400'  # 24 horas
        
        return response
    except Exception as e:
        print(f"Error al leer el archivo {file_path}: {e}")
        raise Http404(f"Error al leer el archivo: {path}")
