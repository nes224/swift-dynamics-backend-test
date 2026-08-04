## Question
![](/assets/q_data_format.png)
## Response Section
ความแตกต่างระหว่าง JSON และ Protocol Buffer
----------------------------------------------------------------------------------------------------------------
|     เปรียบเทียบ                |       JSON (JavaScript Object Notation)  |      Protocol Buffer (Protobuf)     |
----------------------------------------------------------------------------------------------------------------
    รูปแบบข้อมูล (Format)         |      Text-based (ข้อความอ่านออกได้)         |       Binary (รหัสไบนารี ขนาดเล็ก)      | 
  การอ่านด้วยคน (Human Readable) |        Human Readable                    | อ่านไม่ได้โดยตรง ต้องผ่านการ Decode ก่อน   |
   ความเข้มงวดของ Schema        | Optional (Schema-less หรือกึ่ง Schema)      |  Strict Schema (ต้องระบุในไฟล์ .proto)  |
   ความเร็ว & ประสิทธิภาพ         |      ประมวลผลช้ากว่า (ขนาดข้อมูลใหญ่)         |    เร็วกว่ามาก และใช้ bandwidth น้อยกว่า  |
    ลักษณะการใช้งานหลัก           | REST API, Web Application, Configuration |  gRPC, Microservices Communication,  |
                                                                                High-Performance Systems         
    
ข้อดี - ข้อเสียของ JSON
ข้อดี (Pros): 
 - อ่านง่าย เข้าใจง่าย (Human Readable): มนุษย์สามารถอ่านและแก้ไขข้อมูลได้โดยตรงสะดวกต่อการ Debug
 - ยืดหยุ่นสูง (Flexible): ไม่จำเป็นต้องระบุ Schema ล่วงหน้า เพิ่มหรือลด Field ได้ง่าย
 - เป็นมาตรฐานสากล (Universal Support): ภาษาโปรแกรมแทบทุกภาษา รองรับ JSON แบบ Out-of-the-box โดยไม่ต้องติดตั้ง Library เพิ่มเติม
 - เข้ากันได้ดีกับ Web: ทำงานร่วมกับ JavaScript, Frontend Frameworks และ REST API ได้แบบ Native

ข้อเสีย (Cons):
 - ขนาดไฟล์ใหญ่ (Payload Size): เนื่องจากเก็บ Key/Value ในรูปแบบ Text ทำให้มีข้อมูลขยะ (เช่น เครื่องหมายปีกกา, อัญประกาศ) เยอะ
 - การประมวลผลช้ากว่า (Slower Parsing): CPU ต้องใช้พลังงานในการ Parse ข้อความ Text มาเป็น Object
 - ไม่มี Type Safety โดยธรรมชาติ: อาจเกิด Error ในช่วง Runtime ได้หากโครงสร้างข้อมูลฝั่งรับ-ส่งไม่ตรงกัน

ข้อดี - ข้อเสียของ Protocol Buffer (Protobuf)
ข้อดี (Pros):
 - ประสิทธิภาพสูงมาก (High Performance): แปลงเป็น Binary ทำให้ขนาดข้อมูลเล็กกว่า JSON ส่งข้อมูลผ่าน Network ได้เร็วกว่า
 - มี Strict Schema (Type Safety): บังคับใช้ไฟล์ .proto กำหนดโครงสร้างข้อมูลชัดเจน ช่วยลด bugs ฝั่งพัฒนา
 - รองรับ Backward/Forward Compatibility: เพิ่มหรือเปลี่ยน Field ได้โดยระบบเก่าและใหม่ไม่พัง (ยึดตาม Field Tag Number)
 - Auto-generate Code: สามารถสร้าง Code Data Structure ให้กับหลายๆ ภาษาโปรแกรมได้จากไฟล์ .proto เดียวกัน

ข้อเสีย (Cons):
 - อ่านด้วยตาเปล่าไม่ออก (Not Human Readable): ไม่สามารถเปิดดูหรือ Debug ข้อมูลด้วยมือเปล่าได้โดยตรง
 - ต้องใช้ขั้นตอน Compilation: ต้องใช้ protoc ในการ Compile ไฟล์ .proto ก่อนใช้งาน ทำให้มีความซับซ้อนในการตั้งค่า Project
 - ไม่เป็นมิตรกับ Web Browser โดยตรง: Browser ทั่วไปไม่สามารถประมวลผล Protobuf ได้ดีเท่ากับ JSON (ต้องแปลงผ่าน gRPC-Web หรืออื่นๆ)