import random
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Student
from .serializers import StudentDetailSerializer

@api_view(['GET'])
def random_student(request):
    """
    Select a random student based on filters
    Filters: class_id, section_id
    """
    class_id = request.query_params.get('class_id')
    section_id = request.query_params.get('section_id')
    
    if not class_id or not section_id:
        return Response(
            {"error": "Both class_id and section_id are required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get students based on filters
    students = Student.objects.filter(class_name_id=class_id, section_id=section_id)
    
    if not students.exists():
        return Response(
            {"error": "No students found with the given filters"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Select a random student
    random_student = random.choice(students)
    serializer = StudentDetailSerializer(random_student)
    
    return Response(serializer.data)

@api_view(['GET'])
def random_groups(request):
    """
    Create random groups of students based on filters
    Filters: class_id, section_id, group_count
    """
    class_id = request.query_params.get('class_id')
    section_id = request.query_params.get('section_id')
    group_count = request.query_params.get('group_count', 3)
    
    try:
        group_count = int(group_count)
        if group_count < 2:
            group_count = 2
    except (ValueError, TypeError):
        group_count = 3
    
    if not class_id or not section_id:
        return Response(
            {"error": "Both class_id and section_id are required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get students based on filters
    students = list(Student.objects.filter(class_name_id=class_id, section_id=section_id))
    
    if not students:
        return Response(
            {"error": "No students found with the given filters"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Shuffle students
    random.shuffle(students)
    
    # Create groups
    count = min(group_count, len(students))
    groups = [[] for _ in range(count)]
    
    # Distribute students to groups
    for i, student in enumerate(students):
        group_index = i % count
        groups[group_index].append(student)
    
    # Serialize groups
    serialized_groups = []
    for group in groups:
        serialized_groups.append(StudentDetailSerializer(group, many=True).data)
    
    return Response(serialized_groups)
