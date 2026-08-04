## Question
![](/assets/q_acid.png)
## Response Section
1. ความของ ACID คือคุณสมบัติพื้นฐานที่ทำธุรกรรมบนฐานข้อมูล Database Transaction หรือ Atomic หรือ ACID Transaction เป็นการรับประกันความถูกต้องและความน่าเชื่อถือของข้อมูล
    - A (Atomicity) All or Nothing:
        ชุดคำสั่งย่อยทั้งหมดภายใน Transaction เดียวกัน ต้องทำงานเสร็จทั้งหมดทุกขั้นตอน หากมีขั้นตอนใดล้มเหลว ระบบจะต้องทำการย้อนกลับ (Rollback) ข้อมูลทั้งหมด
    - C (Consistency):
        ข้อมูลถูกต้องตามกฏ (Constraints, Invariants, Foreign Keys) ของระบบทั้งก่อนและหลัง ทำ Transaction โดยไม่ยอมให้ข้อมูลที่ไม่ถูกต้อง
        บันทึกลง Database เด็ดขาด
    - I (Isolation):
        การทำงานที่เกิดขึ้นหลาย Transaction (Concurrent Transaction) ต้องไม่ส่งผลกระทบต่อกัน ต้องเสมือนว่าแต่ละ Transaction ทำงาน
        ทีละรายการตามลำดับ (Sequential Execution)
    - D (Durability):
        เมื่อ Transaction ทำการยื่นยันสำเร็จ (Commit) แล้ว ข้อมูลจะถูกบันทึกลงในระบบถาวรและถูกต้อง แม้หลังจากนั้นจะเกิด ไฟดับ หรือ Server Crash ข้อมูลจะต้องไม่สูบหาย
    
2. ความรับผิดชอบระหว่างฝั่ง Database และฝั่ง Application
    ฝั่ง Database รับผิดในเรื่อง:
        1. Atomicity & Durability:
            - ใช้ Mechanism อย่าง Write-Ahead Logging (WAL)/Redo-undo Logs เพื่อคอยบันทึกการเปลี่ยนแปลง
            และใช้ Disk Flushing เพื่อรองรับการ Rollback เมื่อเกิดข้อผิดพลาดหรือ Recover ข้อมูลกลับมาหลัง Crash
        2. Isolation:
            - จัดการเรื่อง ล็อคข้อมูล (Locking Mechanics) เช่น Row-level Locks, Table-level Locks หรือใช้
            Multi-Version Concurrency Control (MVCC) ป้องกันปัญหา Race Condition เช่นพวก Dirty Read, Non-Repeatable Read,
            Phantom Read
        3. Consistency:
            บังรับใช้ Schema Rules, Data Types, Unique Constraints, Foreign Key, Check Constraints
    
    ฝั่ง Application รับผิดในเรื่อง:
        1. Transaction Boundary Management:
            กำหนดจุด Start Begin / Start transaction และ จุดสิ้นสุด Commit / Rollback 
            ของ Transaction ให้ครอบคลุม Business Logic
        2. Consistency:
            ตรวจสอบเงื่อนไขทาง Business Logic ก่อนลง DB เช่น ตรวจสอบว่า User ผู้มีใช้งานมีเงินในบัญชีเพียงพอสำหรับการโอนเงิน หรือ ตัดเงิน
        3. Concurrency Control & Retry Logic:
            ออกแบบการจัดการ Locking บน Application เช่น การ Optimistic Lock โดยใช้ Column version และ ระบบ Retry Mechanism
            ในกรณีที่ DB Deadlock หรือ Serialization Failure
        4. Idempotency & Handing Partial Failures:
            ออกแบบ API ให้เป็น Idempotent รองรับกรณี Network Failure ระหว่าง APP กับ DB
        