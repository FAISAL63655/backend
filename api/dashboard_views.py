from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta

from .models import (
    Student, Attendance, Assignment, Schedule
)

@api_view(['GET'])
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
