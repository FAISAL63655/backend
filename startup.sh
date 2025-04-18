#!/bin/bash
# startup.sh

# Configuración de colores para mejor legibilidad
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== TEACHEASE BACKEND STARTUP ===${NC}"

# Verificar y crear directorios necesarios en el almacenamiento de Render
STORAGE_DIR="/opt/render/project/storage"
MEDIA_DIR="${STORAGE_DIR}/media"
STUDENTS_DIR="${MEDIA_DIR}/students"

if [ -d "${STORAGE_DIR}" ]; then
    echo -e "${GREEN}Directorio de almacenamiento Render encontrado: ${STORAGE_DIR}${NC}"

    # Crear directorios de medios si no existen
    echo -e "${YELLOW}Creando directorios para almacenamiento de medios...${NC}"
    mkdir -p "${MEDIA_DIR}"
    mkdir -p "${STUDENTS_DIR}"

    # Establecer permisos adecuados
    echo -e "${YELLOW}Estableciendo permisos...${NC}"
    chmod -R 755 "${MEDIA_DIR}"

    # Listar los directorios para verificar
    echo -e "${BLUE}Listando directorios de almacenamiento:${NC}"
    echo -e "${YELLOW}Contenido de ${STORAGE_DIR}:${NC}"
    ls -la "${STORAGE_DIR}"

    echo -e "${YELLOW}Contenido de ${MEDIA_DIR}:${NC}"
    ls -la "${MEDIA_DIR}"

    echo -e "${YELLOW}Contenido de ${STUDENTS_DIR}:${NC}"
    if [ -d "${STUDENTS_DIR}" ]; then
        ls -la "${STUDENTS_DIR}"
    else
        echo -e "${RED}El directorio de estudiantes no existe aún.${NC}"
    fi

    echo -e "${GREEN}Directorios de almacenamiento creados y configurados.${NC}"
else
    echo -e "${RED}El directorio de almacenamiento de Render no está disponible.${NC}"
    echo -e "${YELLOW}Intentando crear directorios locales...${NC}"

    # Intentar crear directorios locales
    mkdir -p "media/students"
    chmod -R 755 "media"

    echo -e "${YELLOW}Contenido del directorio actual:${NC}"
    ls -la

    echo -e "${YELLOW}Contenido del directorio media:${NC}"
    ls -la "media"
fi

# Verificar instalación de paquetes
echo -e "${BLUE}Verificando paquetes instalados:${NC}"
pip list | grep -E "whitenoise|pillow|django"

# Ejecutar script para corregir permisos de archivos de medios
echo -e "${BLUE}Ejecutando script para corregir permisos de archivos de medios...${NC}"
python fix_media_permissions.py

# Listar archivos en el directorio de medios después de corregir permisos
echo -e "${BLUE}Listando archivos en el directorio de medios después de corregir permisos:${NC}"
if [ -d "${MEDIA_DIR}" ]; then
    echo -e "${YELLOW}Contenido de ${MEDIA_DIR}:${NC}"
    ls -la "${MEDIA_DIR}"

    if [ -d "${STUDENTS_DIR}" ]; then
        echo -e "${YELLOW}Contenido de ${STUDENTS_DIR}:${NC}"
        ls -la "${STUDENTS_DIR}"
    fi
fi

# Iniciar el servidor con mayor nivel de logging
echo -e "${GREEN}Iniciando el servidor...${NC}"
echo -e "${YELLOW}Usando: gunicorn config.wsgi:application --log-level debug${NC}"
gunicorn config.wsgi:application --log-level debug
