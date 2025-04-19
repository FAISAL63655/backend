from django.urls import re_path
from . import consumers

# تعريف مسارات WebSocket
websocket_urlpatterns = [
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/grades/$', consumers.GradeConsumer.as_asgi()),
    re_path(r'ws/attendance/$', consumers.AttendanceConsumer.as_asgi()),
]
