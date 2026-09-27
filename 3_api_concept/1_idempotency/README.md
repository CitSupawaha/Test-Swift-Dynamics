## Question
![](/assets/q_idempotency.png)
## Response Section

### Idempotency ใน RESTful API

Idempotency คือคุณสมบัติที่ว่า ถ้าเราส่ง request เดิมซ้ำกี่ครั้งก็ตาม ผลลัพธ์ที่ได้จะเหมือนกับส่งแค่ครั้งเดียว ไม่ทำให้เกิด side effect เพิ่ม

ทำไมถึงสำคัญ? ก็เพราะในระบบจริง network ไม่ได้เสถียรเสมอ client อาจ timeout แล้ว retry request ซ้ำ ถ้า API ไม่ idempotent ก็อาจจะเกิดเรื่องแบบ หักเงินซ้ำ, สร้าง order ซ้ำ, ส่ง noti ซ้ำ

ถ้าดูตาม HTTP method แล้ว GET, PUT, DELETE เป็น idempotent โดยธรรมชาติ — GET อ่านข้อมูลเฉยๆ, PUT เขียนทับค่าเดิม, DELETE ลบแล้วลบอีกก็ยังเป็น "ไม่มี" เหมือนเดิม ส่วน POST ไม่เป็น idempotent เพราะมันสร้าง resource ใหม่ทุกครั้ง PATCH ก็ขึ้นอยู่กับว่า implement ยังไง ถ้าเป็น `set value = X` ก็ idempotent แต่ถ้าเป็น `increment value` ก็ไม่

---

### ตัวอย่างการทำ Idempotency สำหรับ POST

วิธีที่นิยมคือให้ client ส่ง Idempotency-Key มาใน header ทุกครั้ง server เอา key ไปเช็คใน cache ว่าเคย process แล้วหรือยัง ถ้าเคยก็คืน response เดิมเลย

```python
import uuid
from functools import wraps

from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


def idempotent(timeout=3600):
    """Decorator ที่ช่วยทำให้ view เป็น idempotent โดยใช้ Idempotency-Key header"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            key = request.headers.get("Idempotency-Key")
            if not key:
                return view_func(self, request, *args, **kwargs)

            cache_key = f"idem:{key}"
            cached = cache.get(cache_key)
            if cached:
                return Response(data=cached["data"], status=cached["status"])

            response = view_func(self, request, *args, **kwargs)

            cache.set(cache_key, {
                "data": response.data,
                "status": response.status_code,
            }, timeout=timeout)

            return response
        return wrapper
    return decorator


class CreateOrderView(APIView):
    """ตัวอย่าง: สร้าง order ถ้า client retry ก็ไม่สร้างซ้ำ"""

    @idempotent(timeout=3600)
    def post(self, request):
        item = request.data.get("item")
        qty = request.data.get("qty", 1)
        return Response(
            {"message": f"Order created: {item} x{qty}"},
            status=status.HTTP_201_CREATED,
        )
```

ฝั่ง client ก็ใช้งานแบบนี้:

```python
import uuid, requests

key = str(uuid.uuid4()) 

resp = requests.post(
    "https://api.example.com/orders/",
    json={"item": "เสื้อยืด", "qty": 2},
    headers={"Idempotency-Key": key},
)

resp2 = requests.post(
    "https://api.example.com/orders/",
    json={"item": "เสื้อยืด", "qty": 2},
    headers={"Idempotency-Key": key}, 
)
```
