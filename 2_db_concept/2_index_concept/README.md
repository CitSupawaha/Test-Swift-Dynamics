## Question
![](/assets/q_indexing.png)
## Response Section

Database Index เป็นโครงสร้างข้อมูลที่ฐานข้อมูลสร้างแยกออกมาจาก table หลัก เพื่อให้ค้นหาข้อมูลได้เร็วขึ้น คล้ายๆ สารบัญหนังสือที่ช่วยให้เราไม่ต้องอ่านทีละหน้าเพื่อหาเรื่องที่ต้องการ

โดยทั่วไป index ที่ใช้กันมากสุดจะเป็นแบบ B-Tree ซึ่งทำให้การค้นหาจาก O(n) เหลือแค่ O(log n) ส่วน Hash Index จะเร็วกว่าอีก O(1) แต่ใช้ได้แค่ exact match เท่านั้น

---

### ข้อดี

**ค้นหาเร็วขึ้นมาก** — query ที่มี WHERE clause บน indexed column จะเร็วขึ้นอย่างเห็นได้ชัด โดยเฉพาะตารางที่มีข้อมูลเยอะ ลองนึกภาพตารางที่มี 5 ล้าน row ถ้าไม่มี index ต้อง scan ทีละ row แต่ถ้ามีก็แค่ไล่ตาม tree structure

**JOIN ทำงานเร็วขึ้น** — ถ้า column ที่ใช้ join มี index อยู่ database จะใช้ index lookup แทนที่จะทำ nested loop scan ทั้งสองตาราง

**เรียงลำดับไม่ต้อง sort ใหม่** — ORDER BY บน indexed column สามารถดึงข้อมูลมาเรียงตาม index ได้เลย ไม่ต้องเสียเวลา sort ในหน่วยความจำ

**บังคับค่าไม่ซ้ำ** — UNIQUE index นอกจากจะช่วยเรื่อง performance แล้ว ยังเป็น constraint ด้วย ป้องกันไม่ให้มีข้อมูลซ้ำ

**Covering Index** — บางทีถ้า query ต้องการแค่ column ที่อยู่ใน index ทั้งหมด DB จะอ่านข้อมูลจาก index ได้เลย ไม่ต้องไป lookup ที่ table จริง ทำให้ลด disk I/O ไปได้เยอะ

---

### ข้อจำกัด

**กิน storage** — index แต่ละตัวก็คือ data structure ที่เก็บแยกจากตาราง ยิ่งมี index เยอะก็ยิ่งใช้ disk เยอะ บางทีขนาด index รวมกันใหญ่กว่า data จริงเลยก็มี

**เขียนช้าลง** — ทุกครั้งที่ INSERT, UPDATE หรือ DELETE database ต้อง update index ด้วย ถ้ามี 5 index ก็ต้อง update 5 ที่ ทำให้ write-heavy workload จะรู้สึกได้

**ไม่ได้ช่วยทุกกรณี** — ถ้า query ดึงข้อมูลเยอะเกิน (เช่น มากกว่า 20-30% ของ table) database อาจเลือก full table scan แทน เพราะ sequential read เร็วกว่า random read ตาม index หรือถ้าใช้ function ครอบ column เช่น `WHERE YEAR(created_at) = 2024` index ก็จะใช้ไม่ได้

**ต้องดูแล** — index ที่ใช้ไปนานๆ อาจเกิด fragmentation ต้อง rebuild เป็นระยะ แล้วก็ต้อง monitor ดูว่า index ตัวไหนไม่ได้ถูกใช้จริง ควรลบทิ้งไม่งั้นมีแต่กินทรัพยากรเปล่าๆ

**เลือกให้ดี** — ถ้าสร้าง index มั่วๆ โดยไม่ดู query pattern ก็ไม่ได้ช่วยอะไร ต้องวิเคราะห์ว่า query ไหนช้า column ไหนถูก filter บ่อย แล้วค่อยสร้าง ใช้ EXPLAIN ดูก่อนว่า query plan เป็นยังไง
