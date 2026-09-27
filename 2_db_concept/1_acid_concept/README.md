## Question
![](/assets/q_acid.png)
## Response Section

ACID เป็นหลักการพื้นฐานที่ใช้รับประกันความถูกต้องของ transaction ในฐานข้อมูล ย่อมาจาก Atomicity, Consistency, Isolation และ Durability

---

### Atomicity

Atomicity คือคุณสมบัติที่ว่า transaction ต้องทำงานแบบ all-or-nothing ถ้า operation ใดใน transaction ล้มเหลว ทุก operation ที่ทำไปก่อนหน้าจะถูก rollback กลับหมดเลย ไม่มีสถานะครึ่งๆ กลางๆ

ตัวอย่างที่เห็นชัดคือการโอนเงิน สมมติหักเงินจากบัญชี A ไป 1,000 บาท แต่พอจะเพิ่มเงินให้บัญชี B กลับ error — ถ้าไม่มี atomicity เงินจะหายไปจาก A โดยที่ B ไม่ได้รับ ซึ่ง database จัดการตรงนี้ผ่าน transaction log (WAL) เพื่อให้ rollback ได้เสมอ

**ฝั่ง DB ดูแล:** การ rollback, transaction log
**ฝั่ง App ดูแล:** กำหนดขอบเขต transaction ให้เหมาะสม (เช่น ใช้ `BEGIN...COMMIT` ให้ครอบคลุม operation ที่ต้องทำพร้อมกัน)

---

### Consistency

Consistency คือการรับประกันว่าข้อมูลจะอยู่ในสถานะที่ถูกต้องเสมอ ทั้งก่อนและหลัง transaction จะไม่มี transaction ไหนทำให้ constraint ที่กำหนดไว้ถูกละเมิดได้

พูดง่ายๆ คือ ถ้าเราตั้ง rule ไว้ว่ายอดเงินห้ามติดลบ ก็จะไม่มี transaction ไหนทำให้ยอดเงินติดลบได้ หรือ foreign key ชี้ไปที่ record ที่ไม่มีอยู่ก็ไม่ได้เช่นกัน

**ฝั่ง DB ดูแล:** บังคับ constraint ต่างๆ เช่น PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL
**ฝั่ง App ดูแล:** business rule ที่ซับซ้อนเกินกว่าจะเขียนเป็น SQL constraint ได้ เช่น validate ว่าจำนวนสินค้าใน stock เพียงพอก่อนสั่งซื้อ

---

### Isolation

Isolation จัดการเรื่อง concurrent transaction หลายๆ transaction ที่ทำงานพร้อมกันจะต้องไม่เห็นข้อมูลที่ยังไม่ commit ของกันและกัน (ขึ้นอยู่กับ isolation level)

ฐานข้อมูลส่วนใหญ่มี 4 ระดับให้เลือก: READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE ยิ่ง level สูงยิ่งปลอดภัยแต่ performance จะลดลง เพราะต้อง lock มากขึ้น

**ฝั่ง DB ดูแล:** locking mechanism และ MVCC ที่จัดการ concurrent access
**ฝั่ง App ดูแล:** เลือกใช้ isolation level ที่เหมาะกับ use case ไม่ใช่ใช้ SERIALIZABLE ไปหมดเพราะจะช้ามาก

---

### Durability

Durability คือเมื่อ transaction commit สำเร็จแล้ว ข้อมูลจะถูกบันทึกถาวร ถึงไฟดับ server ล่ม ข้อมูลก็ยังอยู่ครบ

ฐานข้อมูลทำได้โดยเขียน transaction log ลง disk ก่อนที่จะบอก client ว่า commit สำเร็จ พอ server กลับมาก็อ่าน log แล้ว recover ข้อมูลได้

**ฝั่ง DB ดูแล:** WAL, disk persistence, crash recovery ทั้งหมดเลย
**ฝั่ง App ดูแล:** ไม่ต้องดูแลอะไร ตรงนี้เป็นหน้าที่ DB ล้วนๆ
