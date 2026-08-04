## Question
![](/assets/q_indexing.png)
## Response Section
ข้อดีของการทำ Indexing
    1. เพิ่มประสิทธิภาพในการอ่านข้อมูล (Faster Read Query Performance):
        เปลี่ยนจากการค้นหาแบบไล่อ่านทั้งตาราง (Full Table Scan) ที่มี Time Complexity เป็น O(N) มาเป็นการค้นหาผ่านโครงสร้างข้อมูล เช่น B-Tree / B+Tree ที่มี Time Complexity เพียง O(logN) ช่วยลดระยะเวลาในการค้นหาลงได้
    2. พิ่มความเร็วในการ ORDER BY, GROUP BY และ JOIN:
        เนื่องจาก Index จะจัดเก็บข้อมูลแบบเรียงลำดับไว้อยู่แล้วใน B-Tree ทำให้การทำ Sorting (ORDER BY), Aggregation (GROUP BY), หรือการ JOIN ตารางข้ามกันที่มี Index ตรงกัน ทำได้ทันที ไม่ต้องประมวลผล In-Memory Sort ใหม่
    3. ช่วยรักษาความสมบูรณ์และลดความซ้ำซ้อนของข้อมูล (Enforce Uniqueness):
        การสร้าง Unique Index ช่วยให้ Database ตรวจสอบและป้องกันไม่ให้เกิดข้อมูลซ้ำในระดับ Column ได้อย่างรวดเร็ว (เช่น email, username)
    4. ลดภาระ I/O ของระบบ (Reduce Disk I/O & CPU Utilization):
        เมื่อ Query อ่านบล็อกข้อมูลจาก Disk เฉพาะตำแหน่งที่ Index ชี้ไป ทำให้ช่วยลดการใช้งาน Memory (RAM) และ Disk I/O ลง

ข้อเสียของการทำ Indexing
    1. ส่งผลกระทบต่อความเร็วในการเขียนข้อมูล (Slower Write Operations - INSERT, UPDATE, DELETE):
        ทุกครั้งที่มีการเพิ่ม แก้ไข หรือลบข้อมูล Database ไม่ได้อัปเดตแค่ข้อมูลใน Table หลักอย่างเดียว แต่ต้องทำการอัปเดตและจัดเรียงโครงสร้างข้อมูล Index ใหม่ทั้งหมด
    2. เปลืองพื้นที่จัดเก็บ (Increased Storage / Memory Usage):
        Index ต้องใช้พื้นที่บน Disk และ RAM ในการจัดเก็บโครงสร้าง Tree แยกออกมาต่างหาก หากมีการสร้าง Index มากเกินไป (Over-Indexing) อาจทำให้ขนาดของ Index ใหญ่กว่าขนาดข้อมูลจริงในตาราง
    3. เพิ่มความซับซ้อนและภาระในการบริหารจัดการ (Maintenance Overhead):
        หากมีการสร้าง Index ที่ไม่ได้ถูกใช้งานจริง (Unused Index) หรือ Index มีความซ้ำซ้อน จะสร้าง Overhead ให้ระบบโดยไม่จำเป็น และทำให้ Query Optimizer ประมวลผลหา Execution Plan ช้าลง
    4. ไม่เหมาะกับตารางที่มีขนาดเล็ก หรือ Column ที่มี Cardinality ต่ำ:
        - Small Tables: ตารางที่มีข้อมูลแค่ไม่กี่ร้อยแถว การทำ Full Table Scan อาจเร็วกว่าการไปอ่าน Index แล้วค่อยตามไปอ่าน Table จริง
        - Low Cardinality: คอลัมน์ที่มีค่าซ้ำกันมากๆ (เช่น gender ที่มีแค่ Male/Female, status ที่มีแค่ Active/Inactive) การสร้าง Index จะไม่มีประสิทธิภาพและอาจทำให้ Database Optimizer เลือกที่จะไม่ใช้งาน Index นั้น
