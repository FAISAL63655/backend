import requests
import json
import random
from datetime import datetime

# عنوان الخادم المحلي
BASE_URL = "http://127.0.0.1:8000/api"

def test_batch_create_attendance():
    """
    اختبار نقطة نهاية batch-create للحضور
    """
    print("=== اختبار إنشاء سجلات الحضور المجمعة ===")

    # الحصول على قائمة الطلاب
    response = requests.get(f"{BASE_URL}/students/")
    if response.status_code != 200:
        print(f"خطأ في الحصول على الطلاب: {response.status_code}")
        return

    students = response.json()
    if not students:
        print("لم يتم العثور على طلاب")
        return

    # الحصول على قائمة الفصول
    response = requests.get(f"{BASE_URL}/classes/")
    if response.status_code != 200:
        print(f"خطأ في الحصول على الفصول: {response.status_code}")
        return

    classes = response.json()
    if not classes:
        print("لم يتم العثور على فصول")
        return

    # الحصول على قائمة الأقسام
    response = requests.get(f"{BASE_URL}/sections/")
    if response.status_code != 200:
        print(f"خطأ في الحصول على الأقسام: {response.status_code}")
        return

    sections = response.json()
    if not sections:
        print("لم يتم العثور على أقسام")
        return

    # إنشاء بيانات الحضور
    attendance_data = []
    today = datetime.now().strftime("%Y-%m-%d")

    # اختيار عدد قليل من الطلاب للاختبار
    test_students = students[:3]

    # إنشاء سجلات حضور للطلاب
    for student in test_students:
        attendance_data.append({
            "student": student["id"],
            "date": today,
            "status": random.choice(["present", "absent"]),  # القيم المسموح بها فقط
            "schedule": 1,  # قيمة افتراضية
            "class_name": student["class_name"],
            "section": student["section"]
        })

    # إرسال طلب إنشاء سجلات الحضور المجمعة
    print(f"إرسال {len(attendance_data)} سجلات حضور")
    response = requests.post(
        f"{BASE_URL}/attendances/batch-create/",
        json={"attendance": attendance_data}
    )

    # عرض النتائج
    if response.status_code == 200:
        result = response.json()
        print(f"تم الحفظ بنجاح: {result['success_count']} سجلات")
        if result.get("errors"):
            print(f"أخطاء: {len(result['errors'])}")
            for error in result["errors"]:
                print(f"  - {error}")
    else:
        print(f"خطأ في الطلب: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_batch_create_attendance()
