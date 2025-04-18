from django.db import models
from django.utils import timezone

# Create your models here.

class Class(models.Model):
    """نموذج الصف الدراسي"""
    name = models.CharField(max_length=100, verbose_name="اسم الصف")
    description = models.TextField(blank=True, null=True, verbose_name="وصف الصف")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "صف"
        verbose_name_plural = "صفوف"
        ordering = ['name']

    def __str__(self):
        return self.name

class Section(models.Model):
    """نموذج الفصل الدراسي"""
    name = models.CharField(max_length=100, verbose_name="اسم الفصل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "فصل"
        verbose_name_plural = "فصول"
        ordering = ['name']

    def __str__(self):
        return self.name

class Subject(models.Model):
    """نموذج المادة الدراسية"""
    name = models.CharField(max_length=100, verbose_name="اسم المادة")
    parent_subject = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                                      related_name='sub_subjects', verbose_name="المادة الأساسية")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "مادة"
        verbose_name_plural = "مواد"
        ordering = ['name']

    def __str__(self):
        if self.parent_subject:
            return f"{self.name} ({self.parent_subject.name})"
        return self.name

def validate_image_size(image):
    """التحقق من حجم الصورة (الحد الأقصى 2 ميجابايت)"""
    if image.size > 2 * 1024 * 1024:  # 2MB
        from django.core.exceptions import ValidationError
        raise ValidationError("الحد الأقصى لحجم الصورة هو 2 ميجابايت")

class Student(models.Model):
    """نموذج الطالب"""
    name = models.CharField(max_length=255, verbose_name="اسم الطالب")
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students', verbose_name="الصف")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='students', verbose_name="الفصل")
    image = models.ImageField(
        upload_to='students/',
        blank=True,
        null=True,
        verbose_name="صورة الطالب",
        validators=[validate_image_size]
    )
    status = models.CharField(max_length=20, default='active', verbose_name="حالة الطالب")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "طالب"
        verbose_name_plural = "طلاب"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.class_name} {self.section}"

class Schedule(models.Model):
    """نموذج الجدول الدراسي"""
    DAY_CHOICES = [
        (0, "الأحد"),
        (1, "الإثنين"),
        (2, "الثلاثاء"),
        (3, "الأربعاء"),
        (4, "الخميس"),
    ]

    PERIOD_CHOICES = [
        (1, "الحصة الأولى"),
        (2, "الحصة الثانية"),
        (3, "الحصة الثالثة"),
        (4, "الحصة الرابعة"),
        (5, "الحصة الخامسة"),
        (6, "الحصة السادسة"),
        (7, "الحصة السابعة"),
    ]

    day = models.IntegerField(choices=DAY_CHOICES, verbose_name="اليوم")
    period = models.IntegerField(choices=PERIOD_CHOICES, verbose_name="الحصة")
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='schedules', verbose_name="الصف")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='schedules', verbose_name="الفصل")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='schedules', verbose_name="المادة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "جدول دراسي"
        verbose_name_plural = "جداول دراسية"
        ordering = ['day', 'period']
        unique_together = ['day', 'period', 'class_name', 'section']

    def __str__(self):
        return f"{self.get_day_display()} - {self.get_period_display()} - {self.class_name} {self.section} - {self.subject}"

class Attendance(models.Model):
    """نموذج الحضور والغياب"""
    STATUS_CHOICES = [
        ('present', "حاضر"),
        ('absent', "غائب"),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances', verbose_name="الطالب")
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='attendances', verbose_name="الحصة")
    date = models.DateField(default=timezone.now, verbose_name="التاريخ")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present', verbose_name="الحالة")
    subject_info = models.CharField(max_length=100, blank=True, null=True, verbose_name="اسم المادة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "حضور"
        verbose_name_plural = "حضور"
        ordering = ['-date', 'student__name']
        unique_together = ['student', 'schedule', 'date']

    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"

class Assignment(models.Model):
    """نموذج الواجبات"""
    title = models.CharField(max_length=255, verbose_name="عنوان الواجب")
    description = models.TextField(blank=True, null=True, verbose_name="وصف الواجب")
    due_date = models.DateField(verbose_name="تاريخ التسليم")
    score = models.PositiveIntegerField(default=10, verbose_name="الدرجة")
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='assignments', verbose_name="الحصة")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments', verbose_name="المادة", null=True)
    subject_info = models.CharField(max_length=100, blank=True, null=True, verbose_name="اسم المادة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "واجب"
        verbose_name_plural = "واجبات"
        ordering = ['-due_date', 'title']

    def __str__(self):
        return f"{self.title} - {self.schedule}"

class AssignmentSubmission(models.Model):
    """نموذج تسليم الواجبات"""
    STATUS_CHOICES = [
        ('submitted', "تم التسليم"),
        ('not_submitted', "لم يتم التسليم"),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions', verbose_name="الطالب")
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions', verbose_name="الواجب")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_submitted', verbose_name="حالة التسليم")
    score = models.PositiveIntegerField(default=0, verbose_name="الدرجة")
    subject_info = models.CharField(max_length=100, blank=True, null=True, verbose_name="اسم المادة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "تسليم واجب"
        verbose_name_plural = "تسليمات الواجبات"
        ordering = ['-updated_at']
        unique_together = ['student', 'assignment']

    def __str__(self):
        return f"{self.student} - {self.assignment} - {self.get_status_display()}"

class Grade(models.Model):
    """نموذج الدرجات"""
    TYPE_CHOICES = [
        ('theory', "نظري"),
        ('practical', "تطبيق"),
        ('participation', "مشاركة"),
        ('final', "نهائي"),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades', verbose_name="الطالب")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades', verbose_name="المادة")
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, verbose_name="نوع الدرجة")
    score = models.PositiveIntegerField(default=0, verbose_name="الدرجة")
    max_score = models.PositiveIntegerField(default=100, verbose_name="الدرجة القصوى")
    date = models.DateField(default=timezone.now, verbose_name="التاريخ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "درجة"
        verbose_name_plural = "درجات"
        ordering = ['-date', 'student__name']

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.get_type_display()} - {self.score}/{self.max_score}"

class Note(models.Model):
    """نموذج الملاحظات"""
    TYPE_CHOICES = [
        ('positive', "إيجابية"),
        ('negative', "سلبية"),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='notes', verbose_name="الطالب")
    content = models.TextField(verbose_name="نص الملاحظة")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='positive', verbose_name="نوع الملاحظة")
    date = models.DateField(default=timezone.now, verbose_name="التاريخ")
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='notes', verbose_name="الحصة")
    subject_info = models.CharField(max_length=100, blank=True, null=True, verbose_name="اسم المادة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "ملاحظة"
        verbose_name_plural = "ملاحظات"
        ordering = ['-date', 'student__name']

    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_type_display()}"


class WhiteboardDrawing(models.Model):
    """نموذج رسومات السبورة البيضاء"""
    name = models.CharField(max_length=200, verbose_name="اسم الرسم")
    description = models.TextField(blank=True, null=True, verbose_name="وصف الرسم")
    data = models.TextField(verbose_name="بيانات الرسم")  # JSON data of the drawing
    thumbnail = models.ImageField(upload_to='whiteboard_thumbnails/', blank=True, null=True, verbose_name="صورة مصغرة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "رسم السبورة"
        verbose_name_plural = "رسومات السبورة"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Notification(models.Model):
    """نموذج التنبيهات"""
    TYPE_CHOICES = [
        ('info', "معلومات"),
        ('success', "نجاح"),
        ('warning', "تحذير"),
        ('error', "خطأ"),
    ]

    title = models.CharField(max_length=255, verbose_name="عنوان التنبيه")
    message = models.TextField(verbose_name="نص التنبيه")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='info', verbose_name="نوع التنبيه")
    is_read = models.BooleanField(default=False, verbose_name="تمت القراءة")
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name="رابط")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "تنبيه"
        verbose_name_plural = "تنبيهات"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
