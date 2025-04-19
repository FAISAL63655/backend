import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Notification, Grade, Attendance

class NotificationConsumer(AsyncWebsocketConsumer):
    """
    مستهلك WebSocket للإشعارات
    يسمح بإرسال الإشعارات في الوقت الفعلي
    """
    async def connect(self):
        # الانضمام إلى مجموعة الإشعارات
        await self.channel_layer.group_add(
            "notifications",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # مغادرة مجموعة الإشعارات
        await self.channel_layer.group_discard(
            "notifications",
            self.channel_name
        )

    async def receive(self, text_data):
        # استقبال البيانات من العميل
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', {})
        
        # إرسال الرسالة إلى مجموعة الإشعارات
        await self.channel_layer.group_send(
            "notifications",
            {
                'type': 'notification_message',
                'message': message
            }
        )

    async def notification_message(self, event):
        # إرسال الرسالة إلى WebSocket
        message = event['message']
        
        await self.send(text_data=json.dumps({
            'message': message
        }))

class GradeConsumer(AsyncWebsocketConsumer):
    """
    مستهلك WebSocket للدرجات
    يسمح بإرسال تحديثات الدرجات في الوقت الفعلي
    """
    async def connect(self):
        # الانضمام إلى مجموعة الدرجات
        await self.channel_layer.group_add(
            "grades",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # مغادرة مجموعة الدرجات
        await self.channel_layer.group_discard(
            "grades",
            self.channel_name
        )

    async def receive(self, text_data):
        # استقبال البيانات من العميل
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', {})
        
        # إرسال الرسالة إلى مجموعة الدرجات
        await self.channel_layer.group_send(
            "grades",
            {
                'type': 'grade_message',
                'message': message
            }
        )

    async def grade_message(self, event):
        # إرسال الرسالة إلى WebSocket
        message = event['message']
        
        await self.send(text_data=json.dumps({
            'message': message
        }))

class AttendanceConsumer(AsyncWebsocketConsumer):
    """
    مستهلك WebSocket للحضور
    يسمح بإرسال تحديثات الحضور في الوقت الفعلي
    """
    async def connect(self):
        # الانضمام إلى مجموعة الحضور
        await self.channel_layer.group_add(
            "attendance",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # مغادرة مجموعة الحضور
        await self.channel_layer.group_discard(
            "attendance",
            self.channel_name
        )

    async def receive(self, text_data):
        # استقبال البيانات من العميل
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', {})
        
        # إرسال الرسالة إلى مجموعة الحضور
        await self.channel_layer.group_send(
            "attendance",
            {
                'type': 'attendance_message',
                'message': message
            }
        )

    async def attendance_message(self, event):
        # إرسال الرسالة إلى WebSocket
        message = event['message']
        
        await self.send(text_data=json.dumps({
            'message': message
        }))
