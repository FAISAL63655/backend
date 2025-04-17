# TeachEase Backend

This is the backend API for the TeachEase educational management system, built with Django and Django REST Framework.

## Local Development Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Modify the values as needed

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

## Deployment to Render

### Prerequisites

1. Create a Render account at [render.com](https://render.com)
2. Create a new PostgreSQL database in Render

### Deployment Steps

1. Create a new Web Service in Render
2. Connect your GitHub repository
3. Configure the following settings:
   - **Name**: teachease-backend (or your preferred name)
   - **Environment**: Python
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application`

4. Add the following environment variables:
   - `SECRET_KEY`: Generate a secure random key
   - `DEBUG`: Set to 'False'
   - `ALLOWED_HOSTS`: Your Render domain (e.g., `your-app-name.onrender.com`)
   - `DATABASE_URL`: This will be automatically added by Render if you link your PostgreSQL database
   - `CORS_ALLOWED_ORIGINS`: Your frontend URL (e.g., `https://your-frontend-app.onrender.com`)

5. Deploy the service

## API Documentation

The API provides endpoints for managing:

- Classes and Sections
- Subjects
- Students
- Schedules
- Attendance
- Assignments and Submissions
- Grades
- Notes
- Notifications
- Reports
- Random student picker
- Whiteboard drawings

Access the API at `/api/` when the server is running.

## Project Structure

- `api/`: Main application with models, views, and serializers
- `config/`: Project settings and configuration
- `media/`: User-uploaded files
- `static/`: Static files
- `staticfiles/`: Collected static files for production

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| SECRET_KEY | Django secret key | - |
| DEBUG | Debug mode | False |
| ALLOWED_HOSTS | Comma-separated list of allowed hosts | - |
| DATABASE_URL | Database connection URL | - |
| CORS_ALLOWED_ORIGINS | Comma-separated list of allowed origins for CORS | - |
