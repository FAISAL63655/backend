#!/bin/bash
# startup.sh

# Crear directorios necesarios en el almacenamiento de Render
if [ -d "/opt/render/project/storage" ]; then
    echo "Creando directorios para almacenamiento de medios..."
    mkdir -p /opt/render/project/storage/media
    mkdir -p /opt/render/project/storage/media/students

    # Establecer permisos adecuados
    chmod -R 755 /opt/render/project/storage/media

    # Listar los directorios para verificar
    echo "Listando directorios de almacenamiento:"
    ls -la /opt/render/project/storage
    ls -la /opt/render/project/storage/media

    echo "Directorios de almacenamiento creados y configurados."
else
    echo "El directorio de almacenamiento de Render no está disponible."
fi

# Iniciar el servidor con mayor nivel de logging
echo "Iniciando el servidor..."
gunicorn config.wsgi:application --log-level debug
