from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from datetime import datetime

from .models import Grade, Attendance, AssignmentSubmission
from .serializers import GradeSerializer, GradeDetailSerializer, AttendanceSerializer, AssignmentSubmissionSerializer

@api_view(['GET'])
def get_grades_batch(request):
    """
    Get grades for multiple students at once
    """
    try:
        # Get student IDs from query params
        student_ids_param = request.query_params.get('student_ids', '')
        if not student_ids_param:
            return Response({"error": "student_ids parameter is required"}, status=400)

        # Parse student IDs
        try:
            student_ids = [int(id.strip()) for id in student_ids_param.split(',') if id.strip()]
        except ValueError:
            return Response({"error": "Invalid student_ids format"}, status=400)

        # Get subject ID from query params (optional)
        subject_id = request.query_params.get('subject_id')

        # Build query
        query = Q(student__in=student_ids)
        if subject_id:
            query &= Q(subject=subject_id)

        # Get grades
        grades = Grade.objects.filter(query)

        # Use GradeDetailSerializer for more detailed information
        serializer = GradeDetailSerializer(grades, many=True)

        # Print debug information
        print(f"Batch grades request for students: {student_ids}")
        print(f"Found {len(grades)} grades")
        print(f"Query: {query}")

        # Return results in a format similar to other API endpoints
        return Response({
            "results": serializer.data,
            "count": len(serializer.data)
        })
    except Exception as e:
        print(f"Error in get_grades_batch: {e}")
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def get_attendance_batch(request):
    """
    Get attendance records for a specific date and class/section
    """
    try:
        # Get date from query params
        date_param = request.query_params.get('date')
        if not date_param:
            return Response({"error": "date parameter is required"}, status=400)

        # Parse date
        try:
            date = datetime.strptime(date_param, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        # Get class and section from query params
        class_id = request.query_params.get('class_name')
        section_id = request.query_params.get('section')

        # Build query
        query = Q(date=date)
        if class_id:
            query &= Q(student__class_name=class_id)
        if section_id:
            query &= Q(student__section=section_id)

        # Get attendance records
        attendance_records = Attendance.objects.filter(query)
        serializer = AttendanceSerializer(attendance_records, many=True)

        # Return results in a format similar to other API endpoints
        return Response({
            "results": serializer.data,
            "count": len(serializer.data)
        })
    except Exception as e:
        print(f"Error in get_attendance_batch: {e}")
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def get_submissions_batch(request):
    """
    Get assignment submissions for a specific assignment
    """
    try:
        # Get assignment ID from query params
        assignment_id = request.query_params.get('assignment_id')
        if not assignment_id:
            return Response({"error": "assignment_id parameter is required"}, status=400)

        # Get submissions
        submissions = AssignmentSubmission.objects.filter(assignment=assignment_id)
        serializer = AssignmentSubmissionSerializer(submissions, many=True)

        # Return results in a format similar to other API endpoints
        return Response({
            "results": serializer.data,
            "count": len(serializer.data)
        })
    except Exception as e:
        print(f"Error in get_submissions_batch: {e}")
        return Response({"error": str(e)}, status=500)
