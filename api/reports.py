from django.db.models import Count, Sum, Avg, Q, F
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (
    Student, Class, Section, Subject, 
    Grade, Attendance, Assignment, AssignmentSubmission, Note
)
from .serializers import (
    StudentDetailSerializer, GradeDetailSerializer, 
    AttendanceDetailSerializer, AssignmentSubmissionDetailSerializer,
    NoteDetailSerializer
)

@api_view(['GET'])
def grades_report(request):
    """
    Generate a grades report based on filters
    Filters: class_id, section_id, subject_id, date_from, date_to
    """
    class_id = request.query_params.get('class_id')
    section_id = request.query_params.get('section_id')
    subject_id = request.query_params.get('subject_id')
    date_from = request.query_params.get('date_from')
    date_to = request.query_params.get('date_to', timezone.now().date())
    
    # Base query
    grades = Grade.objects.all()
    
    # Apply filters
    if class_id:
        grades = grades.filter(student__class_name_id=class_id)
    
    if section_id:
        grades = grades.filter(student__section_id=section_id)
    
    if subject_id:
        grades = grades.filter(subject_id=subject_id)
    
    if date_from:
        grades = grades.filter(date__gte=date_from)
    
    grades = grades.filter(date__lte=date_to)
    
    # Group by student and calculate statistics
    students = Student.objects.filter(
        id__in=grades.values_list('student_id', flat=True).distinct()
    )
    
    result = []
    for student in students:
        student_grades = grades.filter(student=student)
        
        # Calculate average score
        total_score = sum(grade.score for grade in student_grades)
        total_max_score = sum(grade.max_score for grade in student_grades)
        
        if total_max_score > 0:
            average_percentage = (total_score / total_max_score) * 100
        else:
            average_percentage = 0
        
        # Get subject names
        subjects = Subject.objects.filter(
            id__in=student_grades.values_list('subject_id', flat=True).distinct()
        )
        subject_scores = {}
        
        for subject in subjects:
            subject_grades = student_grades.filter(subject=subject)
            subject_total_score = sum(grade.score for grade in subject_grades)
            subject_total_max = sum(grade.max_score for grade in subject_grades)
            
            if subject_total_max > 0:
                subject_percentage = (subject_total_score / subject_total_max) * 100
            else:
                subject_percentage = 0
                
            subject_scores[subject.name] = {
                'score': subject_total_score,
                'max_score': subject_total_max,
                'percentage': round(subject_percentage, 2)
            }
        
        result.append({
            'student_id': student.id,
            'student_name': student.name,
            'class_name': student.class_name.name,
            'section_name': student.section.name,
            'total_score': total_score,
            'total_max_score': total_max_score,
            'average_percentage': round(average_percentage, 2),
            'subject_scores': subject_scores,
            'grades_count': student_grades.count()
        })
    
    return Response(result)

@api_view(['GET'])
def attendance_report(request):
    """
    Generate an attendance report based on filters
    Filters: class_id, section_id, date_from, date_to
    """
    class_id = request.query_params.get('class_id')
    section_id = request.query_params.get('section_id')
    date_from = request.query_params.get('date_from')
    date_to = request.query_params.get('date_to', timezone.now().date())
    
    # Base query
    attendances = Attendance.objects.all()
    
    # Apply filters
    if class_id:
        attendances = attendances.filter(student__class_name_id=class_id)
    
    if section_id:
        attendances = attendances.filter(student__section_id=section_id)
    
    if date_from:
        attendances = attendances.filter(date__gte=date_from)
    
    attendances = attendances.filter(date__lte=date_to)
    
    # Group by student and calculate statistics
    students = Student.objects.filter(
        id__in=attendances.values_list('student_id', flat=True).distinct()
    )
    
    result = []
    for student in students:
        student_attendances = attendances.filter(student=student)
        
        # Calculate attendance statistics
        total_days = student_attendances.count()
        present_days = student_attendances.filter(status='present').count()
        absent_days = total_days - present_days
        
        if total_days > 0:
            attendance_percentage = (present_days / total_days) * 100
        else:
            attendance_percentage = 0
        
        result.append({
            'student_id': student.id,
            'student_name': student.name,
            'class_name': student.class_name.name,
            'section_name': student.section.name,
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': absent_days,
            'attendance_percentage': round(attendance_percentage, 2)
        })
    
    return Response(result)

@api_view(['GET'])
def assignments_report(request):
    """
    Generate an assignments report based on filters
    Filters: class_id, section_id, subject_id, date_from, date_to
    """
    class_id = request.query_params.get('class_id')
    section_id = request.query_params.get('section_id')
    subject_id = request.query_params.get('subject_id')
    date_from = request.query_params.get('date_from')
    date_to = request.query_params.get('date_to', timezone.now().date())
    
    # Base query for assignments
    assignments = Assignment.objects.all()
    
    # Apply filters to assignments
    if subject_id:
        assignments = assignments.filter(subject_id=subject_id)
    
    if date_from:
        assignments = assignments.filter(due_date__gte=date_from)
    
    assignments = assignments.filter(due_date__lte=date_to)
    
    # Get relevant schedules based on class and section
    if class_id or section_id:
        schedule_filters = Q()
        if class_id:
            schedule_filters &= Q(schedule__class_name_id=class_id)
        if section_id:
            schedule_filters &= Q(schedule__section_id=section_id)
        assignments = assignments.filter(schedule_filters)
    
    # Get all submissions for these assignments
    submissions = AssignmentSubmission.objects.filter(
        assignment__in=assignments
    )
    
    # Group by student and calculate statistics
    students = Student.objects.filter(
        id__in=submissions.values_list('student_id', flat=True).distinct()
    )
    
    if class_id:
        students = students.filter(class_name_id=class_id)
    
    if section_id:
        students = students.filter(section_id=section_id)
    
    result = []
    for student in students:
        student_submissions = submissions.filter(student=student)
        
        # Calculate submission statistics
        total_assignments = student_submissions.count()
        submitted_count = student_submissions.filter(status='submitted').count()
        not_submitted_count = total_assignments - submitted_count
        
        if total_assignments > 0:
            submission_percentage = (submitted_count / total_assignments) * 100
        else:
            submission_percentage = 0
        
        # Calculate average score
        submitted_with_score = student_submissions.filter(status='submitted')
        total_score = sum(sub.score for sub in submitted_with_score)
        total_max_score = sum(sub.assignment.score for sub in submitted_with_score)
        
        if total_max_score > 0:
            average_percentage = (total_score / total_max_score) * 100
        else:
            average_percentage = 0
        
        result.append({
            'student_id': student.id,
            'student_name': student.name,
            'class_name': student.class_name.name,
            'section_name': student.section.name,
            'assignments_count': total_assignments,
            'submitted_count': submitted_count,
            'not_submitted_count': not_submitted_count,
            'submission_percentage': round(submission_percentage, 2),
            'total_score': total_score,
            'total_max_score': total_max_score,
            'average_percentage': round(average_percentage, 2)
        })
    
    return Response(result)

@api_view(['GET'])
def student_report(request):
    """
    Generate a comprehensive report for a specific student
    Filters: student_id, date_from, date_to
    """
    student_id = request.query_params.get('student_id')
    date_from = request.query_params.get('date_from')
    date_to = request.query_params.get('date_to', timezone.now().date())
    
    if not student_id:
        return Response(
            {"error": "student_id is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response(
            {"error": "Student not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get grades
    grades_query = Grade.objects.filter(student_id=student_id)
    if date_from:
        grades_query = grades_query.filter(date__gte=date_from)
    grades_query = grades_query.filter(date__lte=date_to)
    
    grades = []
    for grade in grades_query:
        grades.append({
            'subject': grade.subject.name,
            'type': grade.get_type_display(),
            'score': f"{grade.score}/{grade.max_score}",
            'percentage': round((grade.score / grade.max_score) * 100, 2) if grade.max_score > 0 else 0,
            'date': grade.date.strftime('%Y-%m-%d')
        })
    
    # Get attendance
    attendance_query = Attendance.objects.filter(student_id=student_id)
    if date_from:
        attendance_query = attendance_query.filter(date__gte=date_from)
    attendance_query = attendance_query.filter(date__lte=date_to)
    
    attendance = []
    for record in attendance_query:
        attendance.append({
            'date': record.date.strftime('%Y-%m-%d'),
            'day': record.schedule.get_day_display(),
            'period': record.schedule.get_period_display(),
            'subject': record.schedule.subject.name,
            'status': record.get_status_display()
        })
    
    # Get assignments
    submissions_query = AssignmentSubmission.objects.filter(student_id=student_id)
    submissions_query = submissions_query.filter(
        assignment__due_date__lte=date_to
    )
    if date_from:
        submissions_query = submissions_query.filter(
            assignment__due_date__gte=date_from
        )
    
    assignments = []
    for submission in submissions_query:
        assignments.append({
            'title': submission.assignment.title,
            'subject': submission.assignment.subject.name if submission.assignment.subject else submission.subject_info,
            'due_date': submission.assignment.due_date.strftime('%Y-%m-%d'),
            'status': submission.get_status_display(),
            'score': f"{submission.score}/{submission.assignment.score}" if submission.status == 'submitted' else '-'
        })
    
    # Get notes
    notes_query = Note.objects.filter(student_id=student_id)
    if date_from:
        notes_query = notes_query.filter(date__gte=date_from)
    notes_query = notes_query.filter(date__lte=date_to)
    
    notes = []
    for note in notes_query:
        notes.append({
            'date': note.date.strftime('%Y-%m-%d'),
            'subject': note.schedule.subject.name if hasattr(note.schedule, 'subject') else note.subject_info,
            'type': note.get_type_display(),
            'content': note.content
        })
    
    # Calculate summary statistics
    total_grades = grades_query.count()
    total_score = sum(grade.score for grade in grades_query)
    total_max_score = sum(grade.max_score for grade in grades_query)
    
    if total_max_score > 0:
        average_percentage = (total_score / total_max_score) * 100
    else:
        average_percentage = 0
    
    total_attendance_days = attendance_query.count()
    present_days = attendance_query.filter(status='present').count()
    absent_days = total_attendance_days - present_days
    
    if total_attendance_days > 0:
        attendance_percentage = (present_days / total_attendance_days) * 100
    else:
        attendance_percentage = 0
    
    total_assignments = submissions_query.count()
    submitted_assignments = submissions_query.filter(status='submitted').count()
    not_submitted_assignments = total_assignments - submitted_assignments
    
    if total_assignments > 0:
        submission_percentage = (submitted_assignments / total_assignments) * 100
    else:
        submission_percentage = 0
    
    # Prepare the response
    result = {
        'student': {
            'id': student.id,
            'name': student.name,
            'class_name': student.class_name.name,
            'section_name': student.section.name
        },
        'summary': {
            'grades': {
                'total': total_grades,
                'average_percentage': round(average_percentage, 2)
            },
            'attendance': {
                'total_days': total_attendance_days,
                'present_days': present_days,
                'absent_days': absent_days,
                'attendance_percentage': round(attendance_percentage, 2)
            },
            'assignments': {
                'total': total_assignments,
                'submitted': submitted_assignments,
                'not_submitted': not_submitted_assignments,
                'submission_percentage': round(submission_percentage, 2)
            }
        },
        'grades': grades,
        'attendance': attendance,
        'assignments': assignments,
        'notes': notes
    }
    
    return Response(result)
