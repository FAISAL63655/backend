#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create static directory if it doesn't exist
mkdir -p static

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Make startup script executable
chmod +x startup.sh
