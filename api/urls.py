from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import reports
from . import random_picker
from . import whiteboard
from . import dashboard_views
from . import champions_views

router = DefaultRouter()
router.register(r'classes', views.ClassViewSet)
router.register(r'sections', views.SectionViewSet)
router.register(r'subjects', views.SubjectViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'schedules', views.ScheduleViewSet)
router.register(r'attendances', views.AttendanceViewSet)
router.register(r'assignments', views.AssignmentViewSet)
router.register(r'assignment-submissions', views.AssignmentSubmissionViewSet)
router.register(r'grades', views.GradeViewSet)
router.register(r'notes', views.NoteViewSet)
router.register(r'notifications', views.NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Reports endpoints
    path('reports/grades/', reports.grades_report, name='grades-report'),
    path('reports/attendance/', reports.attendance_report, name='attendance-report'),
    path('reports/assignments/', reports.assignments_report, name='assignments-report'),
    path('reports/student/', reports.student_report, name='student-report'),

    # Random picker endpoints
    path('random/student/', random_picker.random_student, name='random-student'),
    path('random/groups/', random_picker.random_groups, name='random-groups'),

    # Whiteboard endpoints
    path('whiteboard/drawings/', whiteboard.whiteboard_drawings_list, name='whiteboard-drawings-list'),
    path('whiteboard/drawings/<int:pk>/', whiteboard.whiteboard_drawing_detail, name='whiteboard-drawing-detail'),

    # Dashboard endpoints
    path('dashboard/stats/', dashboard_views.get_dashboard_stats, name='dashboard-stats'),
    path('dashboard/today-schedule/', dashboard_views.get_today_schedule, name='today-schedule'),
    path('dashboard/top-students/', dashboard_views.get_top_students, name='dashboard-top-students'),
    path('dashboard/weekly-attendance/', dashboard_views.get_weekly_attendance, name='dashboard-weekly-attendance'),
    path('dashboard/recent-notes/', dashboard_views.get_recent_notes, name='dashboard-recent-notes'),

    # Champions endpoints
    path('champions/top-attendance/', champions_views.get_top_attendance_students, name='champions-top-attendance'),
    path('champions/top-assignments/', champions_views.get_top_assignment_students, name='champions-top-assignments'),
    path('champions/top-positive-notes/', champions_views.get_top_positive_notes_students, name='champions-top-positive-notes'),
    path('champions/top-grades/', champions_views.get_top_grades_students, name='champions-top-grades'),
    path('champions/top-quran/', champions_views.get_top_quran_students, name='champions-top-quran'),
    path('champions/most-improved/', champions_views.get_most_improved_students, name='champions-most-improved'),
]
