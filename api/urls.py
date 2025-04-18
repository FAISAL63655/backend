from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import reports
from . import random_picker
from . import whiteboard
from . import dashboard_views

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
]
