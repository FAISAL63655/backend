from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q

from .models import (
    Class, Section, Subject, Student, Schedule,
    Attendance, Assignment, AssignmentSubmission,
    Grade, Note, Notification
)
from .serializers import (
    ClassSerializer, SectionSerializer, SubjectSerializer, SubjectDetailSerializer,
    StudentSerializer, StudentDetailSerializer, ScheduleSerializer, ScheduleDetailSerializer,
    AttendanceSerializer, AttendanceDetailSerializer, AssignmentSerializer, AssignmentDetailSerializer,
    AssignmentSubmissionSerializer, AssignmentSubmissionDetailSerializer,
    GradeSerializer, GradeDetailSerializer, NoteSerializer, NoteDetailSerializer,
    NotificationSerializer, NotificationDetailSerializer
)

# Create your views here.
class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SubjectDetailSerializer
        return SubjectSerializer

    @action(detail=False, methods=['get'])
    def main_subjects(self, request):
        main_subjects = Subject.objects.filter(parent_subject__isnull=True)
        serializer = self.get_serializer(main_subjects, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def sub_subjects(self, request, pk=None):
        subject = self.get_object()
        sub_subjects = Subject.objects.filter(parent_subject=subject)
        serializer = self.get_serializer(sub_subjects, many=True)
        return Response(serializer.data)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'class_name__name', 'section__name', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StudentDetailSerializer
        return StudentSerializer

    @action(detail=False, methods=['get'])
    def by_class_section(self, request):
        class_id = request.query_params.get('class_id')
        section_id = request.query_params.get('section_id')

        if class_id and section_id:
            students = Student.objects.filter(class_name_id=class_id, section_id=section_id)
            serializer = StudentDetailSerializer(students, many=True)
            return Response(serializer.data)
        return Response({"error": "Both class_id and section_id are required"}, status=status.HTTP_400_BAD_REQUEST)

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['class_name__name', 'section__name', 'subject__name']
    ordering_fields = ['day', 'period', 'class_name__name', 'section__name']
    ordering = ['day', 'period']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ScheduleDetailSerializer
        return ScheduleSerializer

    @action(detail=False, methods=['get'])
    def current(self, request):
        # Get current day and period
        today = timezone.now().weekday()
        # Map Django's weekday (0=Monday) to our model (0=Sunday)
        today = (today + 1) % 7

        # TODO: Calculate current period based on time
        # For now, just return all periods for today
        schedules = Schedule.objects.filter(day=today)
        serializer = ScheduleDetailSerializer(schedules, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_class_section(self, request):
        class_id = request.query_params.get('class_id')
        section_id = request.query_params.get('section_id')

        if class_id and section_id:
            schedules = Schedule.objects.filter(class_name_id=class_id, section_id=section_id)
            serializer = ScheduleDetailSerializer(schedules, many=True)
            return Response(serializer.data)
        return Response({"error": "Both class_id and section_id are required"}, status=status.HTTP_400_BAD_REQUEST)

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student__name']
    ordering_fields = ['date', 'student__name', 'status']
    ordering = ['-date', 'student__name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AttendanceDetailSerializer
        return AttendanceSerializer

    @action(detail=False, methods=['get'])
    def by_schedule(self, request):
        schedule_id = request.query_params.get('schedule_id')
        date = request.query_params.get('date', timezone.now().date())

        if schedule_id:
            attendances = Attendance.objects.filter(schedule_id=schedule_id, date=date)
            serializer = AttendanceDetailSerializer(attendances, many=True)
            return Response(serializer.data)
        return Response({"error": "schedule_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        student_id = request.query_params.get('student_id')

        if student_id:
            attendances = Attendance.objects.filter(student_id=student_id)
            serializer = AttendanceDetailSerializer(attendances, many=True)
            return Response(serializer.data)
        return Response({"error": "student_id is required"}, status=status.HTTP_400_BAD_REQUEST)

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'title', 'subject__name']
    ordering = ['-due_date', 'title']

    def get_queryset(self):
        queryset = Assignment.objects.all()
        subject_id = self.request.query_params.get('subject')

        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AssignmentDetailSerializer
        return AssignmentSerializer

    @action(detail=False, methods=['get'])
    def by_schedule(self, request):
        schedule_id = request.query_params.get('schedule_id')

        if schedule_id:
            assignments = Assignment.objects.filter(schedule_id=schedule_id)
            serializer = AssignmentDetailSerializer(assignments, many=True)
            return Response(serializer.data)
        return Response({"error": "schedule_id is required"}, status=status.HTTP_400_BAD_REQUEST)

class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student__name', 'assignment__title']
    ordering_fields = ['updated_at', 'student__name', 'status']
    ordering = ['-updated_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AssignmentSubmissionDetailSerializer
        return AssignmentSubmissionSerializer

    @action(detail=False, methods=['get'])
    def by_assignment(self, request):
        assignment_id = request.query_params.get('assignment_id')

        if assignment_id:
            submissions = AssignmentSubmission.objects.filter(assignment_id=assignment_id)
            serializer = AssignmentSubmissionDetailSerializer(submissions, many=True)
            return Response(serializer.data)
        return Response({"error": "assignment_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        student_id = request.query_params.get('student_id')

        if student_id:
            submissions = AssignmentSubmission.objects.filter(student_id=student_id)
            serializer = AssignmentSubmissionDetailSerializer(submissions, many=True)
            return Response(serializer.data)
        return Response({"error": "student_id is required"}, status=status.HTTP_400_BAD_REQUEST)

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student__name', 'subject__name']
    ordering_fields = ['date', 'student__name', 'subject__name', 'type']
    ordering = ['-date', 'student__name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GradeDetailSerializer
        return GradeSerializer

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        student_id = request.query_params.get('student_id')
        subject_id = request.query_params.get('subject_id')

        if student_id:
            grades = Grade.objects.filter(student_id=student_id)
            if subject_id:
                grades = grades.filter(subject_id=subject_id)
            serializer = GradeDetailSerializer(grades, many=True)
            return Response(serializer.data)
        return Response({"error": "student_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_subject(self, request):
        subject_id = request.query_params.get('subject_id')

        if subject_id:
            grades = Grade.objects.filter(subject_id=subject_id)
            serializer = GradeDetailSerializer(grades, many=True)
            return Response(serializer.data)
        return Response({"error": "subject_id is required"}, status=status.HTTP_400_BAD_REQUEST)

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student__name', 'content']
    ordering_fields = ['date', 'student__name', 'type']
    ordering = ['-date', 'student__name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NoteDetailSerializer
        return NoteSerializer

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        student_id = request.query_params.get('student_id')

        if student_id:
            notes = Note.objects.filter(student_id=student_id)
            serializer = NoteDetailSerializer(notes, many=True)
            return Response(serializer.data)
        return Response({"error": "student_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_schedule(self, request):
        schedule_id = request.query_params.get('schedule_id')
        date = request.query_params.get('date', timezone.now().date())

        if schedule_id:
            notes = Note.objects.filter(schedule_id=schedule_id, date=date)
            serializer = NoteDetailSerializer(notes, many=True)
            return Response(serializer.data)
        return Response({"error": "schedule_id is required"}, status=status.HTTP_400_BAD_REQUEST)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'type', 'is_read']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NotificationDetailSerializer
        return NotificationSerializer

    @action(detail=False, methods=['get'])
    def unread(self, request):
        unread_notifications = Notification.objects.filter(is_read=False)
        serializer = NotificationDetailSerializer(unread_notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        serializer = NotificationDetailSerializer(notification)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        Notification.objects.filter(is_read=False).update(is_read=True)
        return Response({"message": "All notifications marked as read"}, status=status.HTTP_200_OK)
