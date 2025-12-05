#CS461: ระบบนับจำนวนสินค้าบนชั้นวางอัตโนมัติ (Automated Shelf Product Counting System)

โปรเจกต์นี้เป็นการพัฒนาระบบ Computer Vision เพื่อตรวจจับและนับจำนวนสินค้าบนชั้นวางของในร้านค้าโดยอัตโนมัติ โดยใช้เทคนิค Object Detection ขั้นสูง (YOLOv8) ซึ่งช่วยลดเวลาและความผิดพลาดในการจัดการสินค้าคงคลัง (Inventory Management)
Frontend Demo: เว็บไซต์สาธิตที่สามารถอัปโหลดรูปภาพและนับจำนวนสินค้าได้ทันที:
URL Demo: https://smart-invertory-ai.netlify.app/

⚙️ วิธีการใช้งานและรันโค้ด (Setup & Run Commands)

โปรเจกต์นี้แบ่งออกเป็น 2 ส่วนหลัก คือ Training (Colab) และ Deployment (Backend API)

1. การเทรนโมเดล (Training via Google Colab)

สำหรับการเทรนโมเดลและประเมินผล ให้ใช้งานผ่าน Colab Notebook:

Colab Link: https://colab.research.google.com/drive/1hy_kScyaJJ2n9DI1-3DLKtuUPaw79gq0

เมื่อรัน Colab Notebook เสร็จสิ้นแล้ว โมเดลที่เทรนสำเร็จ (ไฟล์ best.pt) จะถูกสร้างขึ้น โปรดดาวน์โหลดไฟล์นี้ เพื่อใช้ในขั้นตอนการรัน API ต่อไป

2. การติดตั้งและรัน Web API (Backend)

ส่วนนี้ใช้สำหรับรันเซิร์ฟเวอร์หลังบ้านเพื่อเชื่อมต่อกับเว็บไซต์ Demo (ต้องมีไฟล์ app.py และ best.pt อยู่ในโฟลเดอร์เดียวกัน)

A. การติดตั้ง Dependencies

ติดตั้ง Libraries ที่จำเป็นตามรายการใน requirements.txt:

pip install -r requirements.txt



B. การรัน API Server

รัน Gunicorn (สำหรับ Production Server) โดยชี้ไปที่ไฟล์ app.py:

รัน Flask App (app.py) ด้วย Gunicorn
gunicorn app:app -w 4 -b 0.0.0.0:5000



Endpoint หลัก: เมื่อเว็บไซต์ Frontend ส่งรูปภาพมาที่ POST /detect API จะประมวลผลด้วย best.pt และคืนค่าจำนวนสินค้าที่นับได้ (JSON Output)

3. โครงสร้างไฟล์ที่สำคัญ

ไฟล์โค้ดที่สำคัญใน Repository ได้แก่:

best.pt: ไฟล์โมเดลที่เทรนแล้ว (หัวใจของระบบ)

app.py: โค้ด Backend API

requirements.txt: รายการ Libraries

index.html: โค้ด Frontend Website Demo (Demo URL: https://smart-invertory-ai.netlify.app/)
