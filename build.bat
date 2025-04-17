@echo off
REM Install dependencies
pip install -r requirements.txt

REM Create static directory if it doesn't exist
if not exist static mkdir static

REM Collect static files
python manage.py collectstatic --no-input

REM Apply database migrations
python manage.py migrate
