from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Avg
from datetime import timedelta
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.utils.decorators import method_decorator

from .models import (
    Student, Attendance, Assignment, Schedule, Grade, Note
)

@api_view(['GET'])
@cache_page(settings.CACHE_TTL)  # تخزين مؤقت لمدة 15 دقيقة
def get_dashboard_stats(request):
    """
    Get dashboard statistics:
    - Total number of students
    - Attendance rate
    - Number of active assignments
    """
    # Get total number of students
    total_students = Student.objects.count()

    # Calculate attendance rate for the current week
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    # Get all attendance records for the current week
    attendance_records = Attendance.objects.filter(date__range=[week_start, week_end])

    # Calculate attendance rate
    total_records = attendance_records.count()
    present_records = attendance_records.filter(status='present').count()

    attendance_rate = 0
    if total_records > 0:
        attendance_rate = (present_records / total_records) * 100

    # Get active assignments (due date is today or in the future)
    active_assignments = Assignment.objects.filter(due_date__gte=today).count()

    # Get alerts count (for future implementation)
    alerts_count = 0

    return Response({
        'totalStudents': total_students,
        'attendanceRate': round(attendance_rate, 1),
        'assignmentsCount': active_assignments,
        'alertsCount': alerts_count
    })

@api_view(['GET'])
@cache_page(settings.CACHE_TTL)  # تخزين مؤقت لمدة 15 دقيقة
def get_today_schedule(request):
    """
    Get today's schedule
    """
    # Get current day of the week (0=Monday, 6=Sunday)
    today_weekday = timezone.now().weekday()

    # Map Django's weekday to our model (0=Sunday in our model)
    model_weekday = (today_weekday + 1) % 7

    # Get schedules for today
    try:
        schedules = Schedule.objects.filter(day=model_weekday).select_related(
            'class_name', 'section', 'subject'
        ).order_by('period')

        # Format the response
        result = []
        for schedule in schedules:
            # Get period time based on period number
            period_times = {
                1: "08:00 - 08:45",
                2: "08:45 - 09:30",
                3: "09:30 - 10:15",
                4: "10:15 - 11:00",
                5: "11:00 - 11:45",
                6: "11:45 - 12:30",
                7: "12:30 - 13:15"
            }

            time = period_times.get(schedule.period, f"Period {schedule.period}")

            result.append({
                "id": schedule.id,
                "time": time,
                "subject": schedule.subject.name,
                "class": schedule.class_name.name,
                "section": schedule.section.name,
                "duration": 45,  # Default duration in minutes
                "classId": schedule.class_name.id,
                "sectionId": schedule.section.id,
                "subjectId": schedule.subject.id
            })

        return Response(result)
    except Exception as e:
        # If there's an error, return an empty schedule
        print(f"Error fetching today's schedule: {e}")
        return Response([])

@api_view(['GET'])
@cache_page(settings.CACHE_TTL)  # تخزين مؤقت لمدة 15 دقيقة
def get_top_students(request):
    """
    Get top performing students
    """
    try:
        # Get all students with their grades
        students = Student.objects.all()

        # Calculate average grade for each student
        result = []
        for student in students:
            # Get all grades for this student
            grades = Grade.objects.filter(student=student)

            # Calculate average score
            avg_score = grades.aggregate(avg_score=Avg('score'))

            # Only include students with grades
            if avg_score['avg_score'] is not None:
                result.append({
                    "id": student.id,
                    "name": student.name,
                    "class": student.class_name.name,
                    "section": student.section.name,
                    "avg_score": round(avg_score['avg_score'], 1),
                    "grades_count": grades.count(),
                    "image_url": request.build_absolute_uri(student.image.url) if student.image else None
                })

        # Sort by average score (descending) and take top 5
        result = sorted(result, key=lambda x: x['avg_score'], reverse=True)[:5]

        return Response(result)
    except Exception as e:
        # If there's an error, return an empty list
        print(f"Error fetching top students: {e}")
        return Response([])

@api_view(['GET'])
@cache_page(settings.CACHE_TTL)  # تخزين مؤقت لمدة 15 دقيقة
def get_weekly_attendance(request):
    """
    Get weekly attendance statistics
    """
    try:
        # Get current date
        today = timezone.now().date()

        # Calculate the start of the week (Sunday)
        week_start = today - timedelta(days=today.weekday() + 1)
        if week_start > today:  # If today is Sunday
            week_start = today

        # Calculate the end of the week (Saturday)
        week_end = week_start + timedelta(days=6)

        # Initialize attendance data for each day
        attendance_data = [
            {"day": "الأحد", "day_number": 0, "present": 0, "absent": 0, "rate": 0},
            {"day": "الإثنين", "day_number": 1, "present": 0, "absent": 0, "rate": 0},
            {"day": "الثلاثاء", "day_number": 2, "present": 0, "absent": 0, "rate": 0},
            {"day": "الأربعاء", "day_number": 3, "present": 0, "absent": 0, "rate": 0},
            {"day": "الخميس", "day_number": 4, "present": 0, "absent": 0, "rate": 0},
        ]

        # Get attendance records for the week
        attendance_records = Attendance.objects.filter(date__range=[week_start, week_end])

        # Group attendance records by day
        for record in attendance_records:
            # Get day of week (0=Sunday, 6=Saturday)
            day_of_week = record.date.weekday()
            # Map to our model (0=Sunday, 4=Thursday)
            model_day = (day_of_week + 1) % 7

            # Only count Sunday to Thursday (0-4)
            if model_day <= 4:
                if record.status == 'present':
                    attendance_data[model_day]['present'] += 1
                else:
                    attendance_data[model_day]['absent'] += 1

        # Calculate attendance rate for each day
        for day_data in attendance_data:
            total = day_data['present'] + day_data['absent']
            if total > 0:
                day_data['rate'] = round((day_data['present'] / total) * 100, 1)
            day_data['total'] = total

        return Response(attendance_data)
    except Exception as e:
        # If there's an error, return an empty list
        print(f"Error fetching weekly attendance: {e}")
        return Response([])

@api_view(['GET'])
@cache_page(settings.CACHE_TTL)  # تخزين مؤقت لمدة 15 دقيقة
def get_recent_notes(request):
    """
    Get recent student notes
    """
    try:
        # Get the 10 most recent notes
        notes = Note.objects.all().select_related('student', 'schedule').order_by('-date', '-created_at')[:10]

        # Format the response
        result = []
        for note in notes:
            result.append({
                "id": note.id,
                "student_name": note.student.name,
                "student_id": note.student.id,
                "content": note.content,
                "type": note.type,
                "type_display": note.get_type_display(),
                "date": note.date.strftime("%Y-%m-%d"),
                "subject": note.subject_info or (note.schedule.subject.name if note.schedule and note.schedule.subject else "")
            })

        return Response(result)
    except Exception as e:
        # If there's an error, return an empty list
        print(f"Error fetching recent notes: {e}")
        return Response([])
