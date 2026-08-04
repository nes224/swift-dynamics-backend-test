## Question
![](/assets/q_idempotency.png)
## Response Section
ความหมายของ Idempotency ในบริบทของ RESTful API
    - Idempotency คือ คุณสมบัติของ API ที่แม้นจะถูกเรียกใช้งานด้วย Request เดิม ซ้ำกันหลายครั้ง ผลลัพธ์และสถานะของระบบฝั่ง Server (State) จะยังคงเหมือนกับการเรียกใช้งานเพียงครั้งแรกครั้งเดียว โดยไม่ก่อให้เกิด Side Effect

ความสำคัญในระบบ Back-End:
    - ป้องกันการทำรายการซ้ำ (Duplicate Operations): เช่น ป้องกันการตัดเงินซ้ำในระบบชำระเงิน (Payment Gateway) หรือป้องกันการสร้าง Order ซ้ำ เมื่อ Client กดยืนยันย้ำๆ หรือเกิด Network Retry
    - เพิ่มความน่าเชื่อถือให้ระบบ (Reliability & Fault Tolerance): รองรับกรณี Network Timeout ที่ Client ไม่ได้รับ Response กลับไป จึงทำการ Retry Request เดิมมาใหม่ได้อย่างปลอดภัย

คุณสมบัติ Idempotency ตาม HTTP Methods Standard:
    - GET, HEAD, OPTIONS: เป็นทั้ง Safe และ Idempotent (อ่านอย่างเดียว ไม่เปลี่ยน State บน Server)
    - PUT: เป็น Idempotent (เป็นการ Replace ข้อมูล ณ Resource นั้นๆ เรียกกี่ครั้ง ข้อมูลก็กลายเป็นค่าใหม่เดิม)
    - DELETE: เป็น Idempotent (การลบ Resource เดิมซ้ำๆ ผลลัพธ์คือ Resource นั้นถูกลบไปแล้วเหมือนเดิม)
    - POST: โดยทั่วไป NO Idempotent (การส่ง POST ซ้ำ จะสร้าง Resource ใหม่เพิ่มขึ้นเรื่อยๆ) ดังนั้นจึงนิยมนำกลไก Idempotency Key เข้ามาช่วยควบคุมกรณีที่ต้องการให้ POST มีคุณสมบัติ Idempotency

