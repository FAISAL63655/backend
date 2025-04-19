from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
import logging

# Set up logger
logger = logging.getLogger(__name__)

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
    queryset = Student.objects.select_related('class_name', 'section').all()
    serializer_class = StudentSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'class_name__name', 'section__name', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        """
        تحسين الاستعلام باستخدام select_related لتقليل عدد الاستعلامات
        """
        return Student.objects.select_related('class_name', 'section').all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StudentDetailSerializer
        return StudentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    @action(detail=False, methods=['get'])
    def by_class_section(self, request):
        class_id = request.query_params.get('class_id')
        section_id = request.query_params.get('section_id')

        if class_id and section_id:
            students = Student.objects.select_related('class_name', 'section').filter(class_name_id=class_id, section_id=section_id)
            serializer = StudentDetailSerializer(students, many=True, context={'request': request})
            return Response(serializer.data)
        return Response({"error": "Both class_id and section_id are required"}, status=status.HTTP_400_BAD_REQUEST)

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.select_related('class_name', 'section', 'subject').all()
    serializer_class = ScheduleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['class_name__name', 'section__name', 'subject__name']
    ordering_fields = ['day', 'period', 'class_name__name', 'section__name']
    ordering = ['day', 'period']

    def get_queryset(self):
        """
        تحسين الاستعلام باستخدام select_related لتقليل عدد الاستعلامات
        """
        return Schedule.objects.select_related('class_name', 'section', 'subject').all()

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
        schedules = Schedule.objects.select_related('class_name', 'section', 'subject').filter(day=today)
        serializer = ScheduleDetailSerializer(schedules, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_class_section(self, request):
        class_id = request.query_params.get('class_id')
        section_id = request.query_params.get('section_id')

        if class_id and section_id:
            schedules = Schedule.objects.select_related('class_name', 'section', 'subject').filter(class_name_id=class_id, section_id=section_id)
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

    @action(detail=False, methods=['post'], url_path='batch-create')
    def batch_create(self, request):
        """
        إنشاء أو تحديث مجموعة من سجلات الحضور دفعة واحدة
        """
        try:
            # الحصول على بيانات الحضور من الطلب
            attendance_data = request.data.get('attendance', [])
            if not attendance_data:
                return Response({"error": "No attendance data provided"}, status=status.HTTP_400_BAD_REQUEST)

            # قائمة لتخزين النتائج
            results = []
            errors = []

            # استخدام معاملة قاعدة البيانات
            from django.db import transaction

            # جلب جميع سجلات الحضور الموجودة دفعة واحدة
            student_ids = set()
            dates = set()

            for record in attendance_data:
                if 'student' in record:
                    student_ids.add(record['student'])
                if 'date' in record:
                    dates.add(record['date'])

            # إنشاء قاموس للبحث السريع
            existing_records = {}

            if student_ids and dates:
                # جلب سجلات الحضور الموجودة
                query = Q(student__in=student_ids) & Q(date__in=dates)
                existing_records_query = Attendance.objects.filter(query)

                # تخزين سجلات الحضور الموجودة في قاموس للبحث السريع
                for record in existing_records_query:
                    key = f"{record.student_id}-{record.date}"
                    existing_records[key] = record

            with transaction.atomic():
                for record_data in attendance_data:
                    # التحقق من وجود الحقول المطلوبة
                    if not all(key in record_data for key in ['student', 'date', 'status']):
                        errors.append({"data": record_data, "error": "Missing required fields"})
                        continue

                    try:
                        # البحث عن سجل حضور موجود
                        key = f"{record_data['student']}-{record_data['date']}"
                        existing_record = existing_records.get(key)

                        if existing_record:
                            # تحديث سجل حضور موجود
                            serializer = self.get_serializer(existing_record, data=record_data, partial=True)
                        else:
                            # إنشاء سجل حضور جديد
                            serializer = self.get_serializer(data=record_data)

                        if serializer.is_valid():
                            attendance = serializer.save()
                            results.append(AttendanceDetailSerializer(attendance, context={'request': request}).data)
                        else:
                            errors.append({"data": record_data, "error": serializer.errors})

                    except Exception as e:
                        logger.error(f"Error processing attendance record: {e}")
                        errors.append({"data": record_data, "error": str(e)})

            # إرجاع النتائج والأخطاء
            return Response({
                "results": results,
                "errors": errors,
                "success_count": len(results),
                "error_count": len(errors)
            })

        except Exception as e:
            logger.error(f"Error in batch create attendance: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    """
    API لإدارة درجات الطلاب

    يوفر هذا API عمليات CRUD كاملة لدرجات الطلاب، بالإضافة إلى عمليات مخصصة مثل:
    - الحصول على درجات طالب معين
    - الحصول على درجات مادة معينة
    - عمليات المعالجة المجمعة للدرجات
    """
    queryset = Grade.objects.select_related('student', 'subject').all()
    serializer_class = GradeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student__name', 'subject__name']
    ordering_fields = ['date', 'student__name', 'subject__name', 'type']
    ordering = ['-date', 'student__name']

    def get_queryset(self):
        """
        تحسين الاستعلام باستخدام select_related لتقليل عدد الاستعلامات
        """
        return Grade.objects.select_related('student', 'subject').all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GradeDetailSerializer
        return GradeSerializer

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        student_id = request.query_params.get('student_id')
        subject_id = request.query_params.get('subject_id')

        if student_id:
            grades = Grade.objects.select_related('student', 'subject').filter(student_id=student_id)
            if subject_id:
                grades = grades.filter(subject_id=subject_id)
            serializer = GradeDetailSerializer(grades, many=True)
            return Response(serializer.data)
        return Response({"error": "student_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_subject(self, request):
        subject_id = request.query_params.get('subject_id')

        if subject_id:
            grades = Grade.objects.select_related('student', 'subject').filter(subject_id=subject_id)
            serializer = GradeDetailSerializer(grades, many=True)
            return Response(serializer.data)
        return Response({"error": "subject_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='batch')
    def batch(self, request):
        """
        Get grades for multiple students at once
        """
        try:
            # Get student IDs from query params
            student_ids_param = request.query_params.get('student_ids', '')
            if not student_ids_param:
                return Response({"error": "student_ids parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Parse student IDs
            try:
                student_ids = [int(id.strip()) for id in student_ids_param.split(',') if id.strip()]
            except ValueError:
                return Response({"error": "Invalid student_ids format"}, status=status.HTTP_400_BAD_REQUEST)

            # Get subject ID from query params (optional)
            subject_id = request.query_params.get('subject_id')

            # Build query
            query = Q(student__in=student_ids)
            if subject_id:
                query &= Q(subject=subject_id)

            # Get grades with optimized query
            grades = Grade.objects.select_related('student', 'subject').filter(query)

            # Log debug information
            logger.info(f"Batch grades request for students: {student_ids}")
            logger.info(f"Found {len(grades)} grades")
            logger.info(f"Query: {query}")

            # Use GradeDetailSerializer for more detailed information
            serializer = GradeDetailSerializer(grades, many=True)

            # Return results in a format similar to other API endpoints
            return Response({
                "results": serializer.data,
                "count": len(serializer.data)
            })
        except Exception as e:
            logger.error(f"Error in batch grades endpoint: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='batch-create')
    def batch_create(self, request):
        """
        إنشاء أو تحديث مجموعة من الدرجات دفعة واحدة

        يسمح هذا API بإنشاء أو تحديث مجموعة من الدرجات في طلب واحد، مما يحسن الأداء ويقلل من عدد الطلبات المرسلة إلى الخادم.

        مثال للطلب:
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
            }
          ]
        }
        ```

        مثال للاستجابة:
        ```json
        {
          "results": [
            // مصفوفة من الدرجات التي تم إنشاؤها/تحديثها
          ],
          "errors": [
            // مصفوفة من الأخطاء إن وجدت
          ],
          "success_count": 5,
          "error_count": 0
        }
        ```
        """
        try:
            # الحصول على بيانات الدرجات من الطلب
            grades_data = request.data.get('grades', [])
            if not grades_data:
                return Response({"error": "No grades data provided"}, status=status.HTTP_400_BAD_REQUEST)

            # قائمة لتخزين النتائج
            results = []
            errors = []

            # استخدام معاملة قاعدة البيانات
            from django.db import transaction

            # جلب جميع الدرجات الموجودة دفعة واحدة
            student_ids = set()
            subject_ids = set()
            types = set()
            dates = set()

            for grade_data in grades_data:
                if 'student' in grade_data:
                    student_ids.add(grade_data['student'])
                if 'subject' in grade_data:
                    subject_ids.add(grade_data['subject'])
                if 'type' in grade_data:
                    types.add(grade_data['type'])
                if 'date' in grade_data:
                    dates.add(grade_data['date'])

            # إنشاء قاموس للبحث السريع
            existing_grades = {}

            if student_ids and subject_ids and types:
                # جلب الدرجات الموجودة
                query = Q(student__in=student_ids) & Q(subject__in=subject_ids) & Q(type__in=types)
                if dates:
                    query &= Q(date__in=dates)

                existing_grades_query = Grade.objects.filter(query)

                # تخزين الدرجات الموجودة في قاموس للبحث السريع
                for grade in existing_grades_query:
                    key = f"{grade.student_id}-{grade.subject_id}-{grade.type}-{grade.date}"
                    existing_grades[key] = grade

            with transaction.atomic():
                for grade_data in grades_data:
                    # التحقق من وجود الحقول المطلوبة
                    if not all(key in grade_data for key in ['student', 'subject', 'type', 'score']):
                        errors.append({"data": grade_data, "error": "Missing required fields"})
                        continue

                    try:
                        # البحث عن درجة موجودة
                        date_str = grade_data.get('date', timezone.now().date().isoformat())
                        key = f"{grade_data['student']}-{grade_data['subject']}-{grade_data['type']}-{date_str}"
                        existing_grade = existing_grades.get(key)

                        if existing_grade:
                            # تحديث درجة موجودة
                            serializer = self.get_serializer(existing_grade, data=grade_data, partial=True)
                        else:
                            # إنشاء درجة جديدة
                            serializer = self.get_serializer(data=grade_data)

                        if serializer.is_valid():
                            grade = serializer.save()
                            results.append(GradeDetailSerializer(grade, context={'request': request}).data)
                        else:
                            errors.append({"data": grade_data, "error": serializer.errors})

                    except Exception as e:
                        logger.error(f"Error processing grade: {e}")
                        errors.append({"data": grade_data, "error": str(e)})

            # إرجاع النتائج والأخطاء
            return Response({
                "results": results,
                "errors": errors,
                "success_count": len(results),
                "error_count": len(errors)
            })

        except Exception as e:
            logger.error(f"Error in batch create grades: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
