## Question
![](/assets/q_data_format.png)
## Response Section

### JSON vs Protocol Buffer

JSON กับ Protobuf เป็น data format ที่ใช้งานกันเยอะในระบบ backend แต่มีจุดประสงค์ที่ต่างกันพอสมควร

**JSON** เป็น text format ที่คนอ่านรู้เรื่อง ใช้กันเป็นมาตรฐานใน REST API ทั่วโลก ส่วน **Protobuf** เป็น binary format ของ Google ที่ออกแบบมาเน้นเรื่อง speed กับ size มักใช้คู่กับ gRPC ในการคุยกันระหว่าง microservice

---

### ตัวอย่าง

JSON:
```json
{
  "id": 1,
  "name": "สมชาย",
  "email": "somchai@example.com",
  "age": 25
}
```

Protobuf (.proto schema):
```protobuf
syntax = "proto3";

message User {
  int32 id = 1;
  string name = 2;
  string email = 3;
  int32 age = 4;
}
```

Protobuf ต้องมี schema กำหนดก่อน แล้ว compile ออกมาเป็น code สำหรับภาษาที่ต้องการ ส่วน JSON ไม่ต้อง แค่ส่ง text ตรงๆ ได้เลย

---

### ข้อดี-ข้อเสียของ JSON

ข้อดีหลักๆ ของ JSON คืออ่านง่ายมาก debug สะดวก แค่เปิด browser หรือ Postman ก็เห็นข้อมูลเลย ทุกภาษา ทุก framework รองรับอยู่แล้ว ไม่ต้อง setup อะไรเพิ่ม แล้วก็ยืดหยุ่นสูงเพราะไม่บังคับ schema จะเพิ่มลด field เมื่อไหร่ก็ได้

ข้อเสียคือ payload ใหญ่เพราะเป็น text ทุก key ส่งซ้ำทุก record parse ช้ากว่า binary แล้วก็ไม่มี type safety ถ้าคนส่ง age มาเป็น string "25" แทน number 25 ก็ไม่มีอะไร catch ให้ ต้อง validate เอง

### ข้อดี-ข้อเสียของ Protocol Buffer

ข้อดีคือเล็กมาก เล็กกว่า JSON ได้ 3-10 เท่า serialize/deserialize เร็วกว่า JSON หลายเท่า เหมาะกับ high-throughput system เรื่อง backward compatibility ก็ดีมากเพราะใช้ field number ถ้าเพิ่ม field ใหม่ client เก่าที่ไม่รู้จัก field นั้นก็แค่ skip ไป

ข้อเสียคืออ่านด้วยตาไม่ได้เลย (binary) debug ยากต้องใช้ tool ช่วย decode ต้องเขียน .proto file แล้ว compile ก่อนใช้งาน ซึ่งเพิ่ม step ในการพัฒนา แล้วก็ browser ไม่รองรับ native ถ้าจะใช้กับ frontend ต้อง setup เพิ่ม

---

### สรุปว่าใช้ตัวไหนดี

ถ้าเป็น public REST API หรือ web app ทั่วไป ใช้ JSON ตรงไปตรงมาที่สุด ecosystem ใหญ่ ทุกคนคุ้นเคย

แต่ถ้าเป็น internal service ที่คุยกันเยอะ ต้องการ performance สูง ประหยัด bandwidth เช่น microservice กับ microservice คุยกัน ตรงนี้ Protobuf + gRPC จะเหมาะกว่ามาก
