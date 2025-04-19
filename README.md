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



5. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Modify the values as needed

6. Run migrations:
   ```
   python manage.py migrate
   ```

7. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

8. Run the development server:
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

### Batch Operations

The API supports batch operations for certain resources to improve performance and reduce the number of HTTP requests.

#### Batch Create Grades

**Endpoint**: `POST /api/grades/batch-create/`

**Request Body**:
```json
{
  "grades": [
    {
      "student": 1,
      "subject": 1,
      "date": "2025-04-19",
      "type": "theory",
      "score": 12,
      "max_score": 15
    },
    {
      "student": 1,
      "subject": 1,
      "date": "2025-04-19",
      "type": "practical",
      "score": 4,
      "max_score": 5
    },
    // More grades...
  ]
}
```

**Response**:
```json
{
  "results": [
    // Array of created/updated grade objects
  ],
  "errors": [
    // Array of errors if any
  ],
  "success_count": 5,
  "error_count": 0
}
```

**Notes**:
- This endpoint creates or updates multiple grades in a single request
- If a grade with the same student, subject, type, and date already exists, it will be updated
- The endpoint uses database transactions to ensure data integrity
- The response includes both successful results and errors

#### Batch Create Attendance Records

**Endpoint**: `POST /api/attendances/batch-create/`

**Request Body**:
```json
{
  "attendance": [
    {
      "student": 1,
      "date": "2025-04-19",
      "status": "present",
      "schedule": 1,
      "class_name": 1,
      "section": 1
    },
    {
      "student": 2,
      "date": "2025-04-19",
      "status": "absent",
      "schedule": 1,
      "class_name": 1,
      "section": 1
    },
    // More attendance records...
  ]
}
```

**Response**:
```json
{
  "results": [
    // Array of created/updated attendance records
  ],
  "errors": [
    // Array of errors if any
  ],
  "success_count": 5,
  "error_count": 0
}
```

**Notes**:
- This endpoint creates or updates multiple attendance records in a single request
- If an attendance record with the same student and date already exists, it will be updated
- The endpoint uses database transactions to ensure data integrity
- The response includes both successful results and errors

## Performance Optimizations

- **Database connection pooling**: تحسين اتصالات قاعدة البيانات
- **Static files served with WhiteNoise**: تقديم الملفات الثابتة بكفاءة
- **Optimized database queries**: تحسين استعلامات قاعدة البيانات باستخدام select_related و prefetch_related
- **Efficient file uploads and storage**: رفع وتخزين الملفات بكفاءة
- **Local memory caching**: تخزين مؤقت للبيانات المتكررة باستخدام ذاكرة التخزين المؤقت المحلية
- **Database indexes**: فهارس لتسريع عمليات البحث والترتيب
- **Batch operations**: عمليات معالجة مجمعة لتقليل عدد الطلبات
- **Real-time updates with WebSockets**: تحديثات فورية باستخدام ذاكرة التخزين المؤقت المحلية
- **API Documentation with Swagger**: توثيق شامل لنقاط النهاية API

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

