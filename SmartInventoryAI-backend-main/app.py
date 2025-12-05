import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import io

# 1. ตั้งค่า Logging (เพื่อให้เห็น Error ชัดๆ บน Render)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('YOLO_API')

app = Flask(__name__)

# 2. ตั้งค่า CORS (อนุญาตให้เว็บหน้าบ้านคุยกับหลังบ้านได้)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# 3. โหลดโมเดล
logger.info("⏳ กำลังโหลดโมเดล bestNew.pt ...")
try:
    # ตรวจสอบให้แน่ใจว่าไฟล์ bestNew.pt อยู่โฟลเดอร์เดียวกับไฟล์นี้
    model = YOLO('bestNew.pt') 
    logger.info("✅ โหลดโมเดลสำเร็จ!")
except Exception as e:
    logger.error(f"❌ โหลดโมเดลพัง: {e}")
    # หมายเหตุ: ถ้าไฟล์ไม่มี มันจะ Error ตรงนี้

@app.route("/")
def home():
    return "YOLOv8 API is running! (Model: bestNew.pt)"
# ❌ เกิดข้อผิดพลาด: API Error: {"error":"name 'model' is not defined"}
@app.route("/detect", methods=["POST", "OPTIONS"])
def detect():
    # จัดการ Preflight Request (สำหรับ Browser ที่เข้มงวด)
    if request.method == "OPTIONS":
        response = jsonify({"message": "OK"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    
    try:
        # อ่านไฟล์รูปภาพ
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))

        # ---------------------------------------------------------
        # [จุดสำคัญ] สั่งให้ AI ทำงานตามสูตรของคุณ
        # ---------------------------------------------------------
        logger.info("🔍 กำลังวิเคราะห์ภาพ (conf=0.25, iou=0.45)...")
        results = model(image, conf=0.25, iou=0.45) 
        
        # แกะกล่องของขวัญ (ผลลัพธ์)
        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                label = model.names[cls_id]

                detections.append({
                    "label": label,
                    "confidence": conf,
                    "box": [x1, y1, x2, y2]
                })

        count = len(detections)
        logger.info(f"💡 เจอวัตถุทั้งหมด: {count} ชิ้น")
        
        # ส่ง JSON กลับไปให้หน้าบ้าน
        response = jsonify({
            "count": count,
            "detections": detections
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # ใช้ Port ตามที่ Render กำหนด (สำคัญมาก ห้ามแก้)
    port = int(os.environ.get("PORT", 5000))

    app.run(host='0.0.0.0', port=port)
