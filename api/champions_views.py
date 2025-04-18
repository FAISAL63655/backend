from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Q, Sum, Avg, F
from django.utils import timezone
from datetime import timedelta

from .models import (
    Student, Attendance, Assignment, AssignmentSubmission, Note, Grade
)

@api_view(['GET'])
def get_top_attendance_students(request):
    """
    Get top 5 students with highest attendance rate
    """
    try:
        # Get current semester start date (for example, last 3 months)
        today = timezone.now().date()
        semester_start = today - timedelta(days=90)
        
        # Get all students
        students = Student.objects.all()
        
        # Calculate attendance rate for each student
        result = []
        for student in students:
            # Get attendance records for this student
            attendance_records = Attendance.objects.filter(
                student=student,
                date__gte=semester_start
            )
            
            total_records = attendance_records.count()
            if total_records > 0:
                present_records = attendance_records.filter(status='present').count()
                attendance_rate = (present_records / total_records) * 100
                
                result.append({
                    "id": student.id,
                    "name": student.name,
                    "class": student.class_name.name if student.class_name else "",
                    "section": student.section.name if student.section else "",
                    "image": request.build_absolute_uri(student.image.url) if student.image else None,
                    "attendance_rate": round(attendance_rate, 1),
                    "present_days": present_records,
                    "total_days": total_records
                })
        
        # Sort by attendance rate (descending) and take top 5
        result = sorted(result, key=lambda x: x['attendance_rate'], reverse=True)[:5]
        
        return Response(result)
    except Exception as e:
        print(f"Error fetching top attendance students: {e}")
        return Response([])

@api_view(['GET'])
def get_top_assignment_students(request):
    """
    Get top 5 students with highest assignment submission rate
    """
    try:
        # Get current semester start date (for example, last 3 months)
        today = timezone.now().date()
        semester_start = today - timedelta(days=90)
        
        # Get all students
        students = Student.objects.all()
        
        # Calculate assignment submission rate for each student
        result = []
        for student in students:
            # Get assignment submissions for this student
            submissions = AssignmentSubmission.objects.filter(
                student=student,
                created_at__gte=semester_start
            )
            
            # Get total assignments assigned to this student's class
            student_class = student.class_name
            student_section = student.section
            if student_class and student_section:
                total_assignments = Assignment.objects.filter(
                    Q(class_name=student_class) & 
                    (Q(section=student_section) | Q(section=None)),
                    created_at__gte=semester_start
                ).count()
                
                if total_assignments > 0:
                    submitted_assignments = submissions.filter(status='submitted').count()
                    submission_rate = (submitted_assignments / total_assignments) * 100
                    
                    result.append({
                        "id": student.id,
                        "name": student.name,
                        "class": student_class.name,
                        "section": student_section.name,
                        "image": request.build_absolute_uri(student.image.url) if student.image else None,
                        "submission_rate": round(submission_rate, 1),
                        "submitted_assignments": submitted_assignments,
                        "total_assignments": total_assignments
                    })
        
        # Sort by submission rate (descending) and take top 5
        result = sorted(result, key=lambda x: x['submission_rate'], reverse=True)[:5]
        
        return Response(result)
    except Exception as e:
        print(f"Error fetching top assignment students: {e}")
        return Response([])

@api_view(['GET'])
def get_top_positive_notes_students(request):
    """
    Get top 5 students with highest number of positive notes
    """
    try:
        # Get current semester start date (for example, last 3 months)
        today = timezone.now().date()
        semester_start = today - timedelta(days=90)
        
        # Get students with positive notes count
        students_with_notes = Student.objects.annotate(
            positive_notes_count=Count(
                'note',
                filter=Q(note__type='positive', note__date__gte=semester_start)
            )
        ).filter(positive_notes_count__gt=0).order_by('-positive_notes_count')[:5]
        
        # Format the response
        result = []
        for student in students_with_notes:
            result.append({
                "id": student.id,
                "name": student.name,
                "class": student.class_name.name if student.class_name else "",
                "section": student.section.name if student.section else "",
                "image": request.build_absolute_uri(student.image.url) if student.image else None,
                "positive_notes_count": student.positive_notes_count
            })
        
        return Response(result)
    except Exception as e:
        print(f"Error fetching top positive notes students: {e}")
        return Response([])

@api_view(['GET'])
def get_top_grades_students(request):
    """
    Get top 5 students with highest average grades
    """
    try:
        # Get current semester start date (for example, last 3 months)
        today = timezone.now().date()
        semester_start = today - timedelta(days=90)
        
        # Get students with average grades
        students_with_grades = Student.objects.annotate(
            avg_grade=Avg('grade__score', filter=Q(grade__created_at__gte=semester_start))
        ).filter(avg_grade__isnull=False).order_by('-avg_grade')[:5]
        
        # Format the response
        result = []
        for student in students_with_grades:
            result.append({
                "id": student.id,
                "name": student.name,
                "class": student.class_name.name if student.class_name else "",
                "section": student.section.name if student.section else "",
                "image": request.build_absolute_uri(student.image.url) if student.image else None,
                "avg_grade": round(student.avg_grade, 1),
                "grade_count": Grade.objects.filter(student=student, created_at__gte=semester_start).count()
            })
        
        return Response(result)
    except Exception as e:
        print(f"Error fetching top grades students: {e}")
        return Response([])

@api_view(['GET'])
def get_top_quran_students(request):
    """
    Get top 5 students with highest Quran grades
    """
    try:
        # Get current semester start date (for example, last 3 months)
        today = timezone.now().date()
        semester_start = today - timedelta(days=90)
        
        # Get students with average Quran grades
        students_with_quran_grades = Student.objects.annotate(
            avg_quran_grade=Avg(
                'grade__score', 
                filter=Q(
                    grade__created_at__gte=semester_start,
                    grade__type='quran'
                )
            )
        ).filter(avg_quran_grade__isnull=False).order_by('-avg_quran_grade')[:5]
        
        # Format the response
        result = []
        for student in students_with_quran_grades:
            result.append({
                "id": student.id,
                "name": student.name,
                "class": student.class_name.name if student.class_name else "",
                "section": student.section.name if student.section else "",
                "image": request.build_absolute_uri(student.image.url) if student.image else None,
                "avg_quran_grade": round(student.avg_quran_grade, 1),
                "quran_grade_count": Grade.objects.filter(
                    student=student, 
                    type='quran',
                    created_at__gte=semester_start
                ).count()
            })
        
        return Response(result)
    except Exception as e:
        print(f"Error fetching top Quran students: {e}")
        return Response([])

@api_view(['GET'])
def get_most_improved_students(request):
    """
    Get top 5 students with most improvement in grades
    """
    try:
        # Get current semester start date (for example, last 3 months)
        today = timezone.now().date()
        semester_start = today - timedelta(days=90)
        mid_semester = semester_start + (today - semester_start) / 2
        
        # Get all students
        students = Student.objects.all()
        
        # Calculate improvement for each student
        result = []
        for student in students:
            # Get early semester grades
            early_grades = Grade.objects.filter(
                student=student,
                created_at__gte=semester_start,
                created_at__lt=mid_semester
            )
            
            # Get late semester grades
            late_grades = Grade.objects.filter(
                student=student,
                created_at__gte=mid_semester
            )
            
            if early_grades.count() > 0 and late_grades.count() > 0:
                early_avg = early_grades.aggregate(avg=Avg('score'))['avg'] or 0
                late_avg = late_grades.aggregate(avg=Avg('score'))['avg'] or 0
                
                improvement = late_avg - early_avg
                
                if improvement > 0:
                    result.append({
                        "id": student.id,
                        "name": student.name,
                        "class": student.class_name.name if student.class_name else "",
                        "section": student.section.name if student.section else "",
                        "image": request.build_absolute_uri(student.image.url) if student.image else None,
                        "improvement": round(improvement, 1),
                        "early_avg": round(early_avg, 1),
                        "late_avg": round(late_avg, 1)
                    })
        
        # Sort by improvement (descending) and take top 5
        result = sorted(result, key=lambda x: x['improvement'], reverse=True)[:5]
        
        return Response(result)
    except Exception as e:
        print(f"Error fetching most improved students: {e}")
        return Response([])
