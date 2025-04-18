"""
Paquete de vistas para la API.
"""

# Importar todos los ViewSets desde el archivo views.py principal
from ..views import (
    ClassViewSet,
    SectionViewSet,
    SubjectViewSet,
    StudentViewSet,
    ScheduleViewSet,
    AttendanceViewSet,
    AssignmentViewSet,
    AssignmentSubmissionViewSet,
    GradeViewSet,
    NoteViewSet,
    NotificationViewSet
)

# Exportar todos los ViewSets para que sean accesibles desde api.views
__all__ = [
    'ClassViewSet',
    'SectionViewSet',
    'SubjectViewSet',
    'StudentViewSet',
    'ScheduleViewSet',
    'AttendanceViewSet',
    'AssignmentViewSet',
    'AssignmentSubmissionViewSet',
    'GradeViewSet',
    'NoteViewSet',
    'NotificationViewSet'
]
