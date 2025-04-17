from django.contrib import admin
from .models import (
    Class, Section, Subject, Student, Schedule,
    Attendance, Assignment, AssignmentSubmission,
    Grade, Note
)

# Register your models here.
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_subject', 'created_at')
    list_filter = ('parent_subject',)
    search_fields = ('name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_name', 'section', 'created_at')
    list_filter = ('class_name', 'section')
    search_fields = ('name',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('get_day_display', 'get_period_display', 'class_name', 'section', 'subject')
    list_filter = ('day', 'period', 'class_name', 'section', 'subject')
    search_fields = ('class_name__name', 'section__name', 'subject__name')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'schedule', 'date', 'status')
    list_filter = ('status', 'date', 'schedule')
    search_fields = ('student__name',)
    date_hierarchy = 'date'

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'schedule', 'due_date', 'score')
    list_filter = ('schedule', 'due_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'due_date'

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'status', 'score')
    list_filter = ('status', 'assignment')
    search_fields = ('student__name', 'assignment__title')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'type', 'score', 'max_score', 'date')
    list_filter = ('type', 'subject', 'date')
    search_fields = ('student__name',)
    date_hierarchy = 'date'

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('student', 'type', 'content', 'date', 'schedule')
    list_filter = ('type', 'date', 'schedule')
    search_fields = ('student__name', 'content')
    date_hierarchy = 'date'
