from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        # إضافة فهارس للحقول المستخدمة بشكل متكرر في عمليات البحث والترتيب
        
        # فهارس للطلاب
        migrations.AddIndex(
            model_name='student',
            index=models.Index(fields=['name'], name='student_name_idx'),
        ),
        migrations.AddIndex(
            model_name='student',
            index=models.Index(fields=['class_name', 'section'], name='student_class_section_idx'),
        ),
        
        # فهارس للجدول الدراسي
        migrations.AddIndex(
            model_name='schedule',
            index=models.Index(fields=['day', 'period'], name='schedule_day_period_idx'),
        ),
        migrations.AddIndex(
            model_name='schedule',
            index=models.Index(fields=['class_name', 'section'], name='schedule_class_section_idx'),
        ),
        
        # فهارس للحضور
        migrations.AddIndex(
            model_name='attendance',
            index=models.Index(fields=['student', 'date'], name='attendance_student_date_idx'),
        ),
        migrations.AddIndex(
            model_name='attendance',
            index=models.Index(fields=['date', 'status'], name='attendance_date_status_idx'),
        ),
        
        # فهارس للواجبات
        migrations.AddIndex(
            model_name='assignment',
            index=models.Index(fields=['due_date'], name='assignment_due_date_idx'),
        ),
        migrations.AddIndex(
            model_name='assignment',
            index=models.Index(fields=['subject'], name='assignment_subject_idx'),
        ),
        
        # فهارس للدرجات
        migrations.AddIndex(
            model_name='grade',
            index=models.Index(fields=['student', 'subject'], name='grade_student_subject_idx'),
        ),
        migrations.AddIndex(
            model_name='grade',
            index=models.Index(fields=['student', 'type'], name='grade_student_type_idx'),
        ),
        migrations.AddIndex(
            model_name='grade',
            index=models.Index(fields=['date'], name='grade_date_idx'),
        ),
        
        # فهارس للملاحظات
        migrations.AddIndex(
            model_name='note',
            index=models.Index(fields=['student', 'date'], name='note_student_date_idx'),
        ),
        migrations.AddIndex(
            model_name='note',
            index=models.Index(fields=['type'], name='note_type_idx'),
        ),
        
        # فهارس للإشعارات
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['is_read'], name='notification_is_read_idx'),
        ),
    ]
