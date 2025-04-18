from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Avg, Q
from datetime import timedelta

from .models import (
    Student, Attendance, Assignment, AssignmentSubmission
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
    # This is a placeholder for the actual implementation
    # In a real implementation, you would fetch the schedule for the current day
    
    # Get current day of the week (0=Monday, 6=Sunday)
    today_weekday = timezone.now().weekday()
    
    # Map Django's weekday to our model (0=Sunday in our model)
    model_weekday = (today_weekday + 1) % 7
    
    # For now, return a simple response
    # In the future, you can implement this to return the actual schedule
    return Response([
        {
            "id": 1,
            "time": "08:00 - 08:45",
            "subject": "الرياضيات",
            "class": "الصف الثالث",
            "section": "أ"
        },
        {
            "id": 2,
            "time": "08:45 - 09:30",
            "subject": "العلوم",
            "class": "الصف الرابع",
            "section": "ب"
        },
        {
            "id": 3,
            "time": "09:30 - 10:15",
            "subject": "اللغة العربية",
            "class": "الصف الخامس",
            "section": "أ"
        },
        {
            "id": 4,
            "time": "10:15 - 11:00",
            "subject": "التربية الإسلامية",
            "class": "الصف السادس",
            "section": "ج"
        }
    ])
