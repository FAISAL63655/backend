from rest_framework import serializers
from .models import (
    Class, Section, Subject, Student, Schedule,
    Attendance, Assignment, AssignmentSubmission,
    Grade, Note, WhiteboardDrawing, Notification
)

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class SubjectDetailSerializer(serializers.ModelSerializer):
    parent_subject_name = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = '__all__'

    def get_parent_subject_name(self, obj):
        if obj.parent_subject:
            return obj.parent_subject.name
        return None

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentDetailSerializer(serializers.ModelSerializer):
    class_name_display = serializers.CharField(source='class_name.name', read_only=True)
    section_display = serializers.CharField(source='section.name', read_only=True)

    class Meta:
        model = Student
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

class ScheduleDetailSerializer(serializers.ModelSerializer):
    day_display = serializers.CharField(source='get_day_display', read_only=True)
    period_display = serializers.CharField(source='get_period_display', read_only=True)
    class_name_display = serializers.CharField(source='class_name.name', read_only=True)
    section_display = serializers.CharField(source='section.name', read_only=True)
    subject_display = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Schedule
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class AttendanceDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class AssignmentDetailSerializer(serializers.ModelSerializer):
    schedule_display = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = '__all__'

    def get_schedule_display(self, obj):
        return str(obj.schedule)

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = '__all__'

class AssignmentSubmissionDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class GradeDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Grade
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class NoteDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Note
        fields = '__all__'


class WhiteboardDrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhiteboardDrawing
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class NotificationDetailSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
