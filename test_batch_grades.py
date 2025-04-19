import requests
import json
import random
from datetime import datetime

# عنوان الخادم المحلي
BASE_URL = "http://127.0.0.1:8000/api"

def test_batch_create_grades():
    """
    اختبار نقطة نهاية batch-create للدرجات
    """
    print("=== اختبار إنشاء الدرجات المجمعة ===")
    
    # الحصول على قائمة الطلاب
    response = requests.get(f"{BASE_URL}/students/")
    if response.status_code != 200:
        print(f"خطأ في الحصول على الطلاب: {response.status_code}")
        return
    
    students = response.json()
    if not students:
        print("لم يتم العثور على طلاب")
        return
    
    # الحصول على قائمة المواد
    response = requests.get(f"{BASE_URL}/subjects/")
    if response.status_code != 200:
        print(f"خطأ في الحصول على المواد: {response.status_code}")
        return
    
    subjects = response.json()
    if not subjects:
        print("لم يتم العثور على مواد")
        return
    
    # إنشاء بيانات الدرجات
    grades_data = []
    today = datetime.now().strftime("%Y-%m-%d")
    
    # اختيار طالب واحد وموضوع واحد للاختبار
    student = students[0]
    subject = subjects[0]
    
    # إنشاء درجات لأنواع مختلفة
    grade_types = [
        {"type": "theory", "score": random.randint(0, 15), "max_score": 15},
        {"type": "practical", "score": random.randint(0, 5), "max_score": 5},
        {"type": "participation", "score": random.randint(0, 10), "max_score": 10},
        {"type": "quran", "score": random.randint(0, 20), "max_score": 20},
        {"type": "final", "score": random.randint(0, 40), "max_score": 40}
    ]
    
    for grade_type in grade_types:
        grades_data.append({
            "student": student["id"],
            "subject": subject["id"],
            "date": today,
            "type": grade_type["type"],
            "score": grade_type["score"],
            "max_score": grade_type["max_score"]
        })
    
    # إرسال طلب إنشاء الدرجات المجمعة
    print(f"إرسال {len(grades_data)} درجات للطالب {student['name']} في المادة {subject['name']}")
    response = requests.post(
        f"{BASE_URL}/grades/batch-create/",
        json={"grades": grades_data}
    )
    
    # عرض النتائج
    if response.status_code == 200:
        result = response.json()
        print(f"تم الحفظ بنجاح: {result['success_count']} درجات")
        if result.get("errors"):
            print(f"أخطاء: {len(result['errors'])}")
            for error in result["errors"]:
                print(f"  - {error}")
    else:
        print(f"خطأ في الطلب: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_batch_create_grades()
