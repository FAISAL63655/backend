import requests
import time
import statistics

# عنوان الخادم المحلي
BASE_URL = "http://127.0.0.1:8000/api"

def measure_response_time(url, method="get", data=None, iterations=5):
    """
    قياس زمن الاستجابة لنقطة نهاية API
    """
    times = []
    
    for i in range(iterations):
        start_time = time.time()
        
        if method.lower() == "get":
            response = requests.get(url)
        elif method.lower() == "post":
            response = requests.post(url, json=data)
        
        end_time = time.time()
        
        if response.status_code == 200:
            times.append(end_time - start_time)
        else:
            print(f"Error: {response.status_code} - {response.text}")
    
    if times:
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"URL: {url}")
        print(f"  Average response time: {avg_time:.4f} seconds")
        print(f"  Min response time: {min_time:.4f} seconds")
        print(f"  Max response time: {max_time:.4f} seconds")
        print(f"  Status code: {response.status_code}")
        print()
        
        return avg_time
    
    return None

def test_api_performance():
    """
    اختبار أداء نقاط النهاية API
    """
    print("=== اختبار أداء نقاط النهاية API ===")
    
    # اختبار نقاط النهاية الرئيسية
    endpoints = [
        "/classes/",
        "/sections/",
        "/subjects/",
        "/students/",
        "/schedules/",
        "/attendances/",
        "/assignments/",
        "/grades/",
        "/notes/",
        "/dashboard/stats/",
        "/dashboard/today-schedule/",
        "/dashboard/top-students/",
    ]
    
    for endpoint in endpoints:
        measure_response_time(f"{BASE_URL}{endpoint}")
    
    # اختبار نقاط النهاية المجمعة
    # الحصول على معرفات الطلاب
    response = requests.get(f"{BASE_URL}/students/")
    if response.status_code == 200:
        students = response.json()
        if students:
            student_ids = ",".join([str(student["id"]) for student in students[:5]])
            
            # اختبار نقطة نهاية الدرجات المجمعة
            measure_response_time(f"{BASE_URL}/grades/batch/?student_ids={student_ids}")

if __name__ == "__main__":
    # تشغيل الخادم قبل تشغيل هذا الاختبار
    test_api_performance()
