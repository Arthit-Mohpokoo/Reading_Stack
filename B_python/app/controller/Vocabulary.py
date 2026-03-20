from fastapi import UploadFile, File, Form, HTTPException
from app.config.model import collectionVocabulary ,collectionVocabularyReview
import shutil , uuid,os
from bson import ObjectId
from datetime import datetime
#uuid เอาสุมชื่อไฟล์ไม่ซ้ำกัน

ALLOWED_EXT = {".png", ".jpg", ".jpeg", ".webp"}
UPLOAD_DIR = "app/upload/read_img/"

async def vocabC(
    name: str = Form(...),
    read: str = Form(...),
    images: UploadFile = File(None)
):
    try:
        if not name:
            raise HTTPException(status_code=409, detail="กรุณากรอกชื่อให้เรียบร้อย")
        if not read:
            raise HTTPException(status_code=409, detail="กรุณากรอกคำอ่านให้เรียบร้อย")
        img_path = None
        if images:
            ext = os.path.splitext(images.filename)[1].lower()  # .png .jpg
            if ext not in ALLOWED_EXT:
                raise HTTPException(status_code=403, detail="ไม่สามารถเพิ่มรูปได้")
            filename = f"{uuid.uuid4()}{ext}" 
            img_path = f"{UPLOAD_DIR}{filename}"
            
            with open(img_path, "wb") as f:
                shutil.copyfileobj(images.file, f)
            #shutil.copyfileobj คัดลอกข้อมูลจาก file object หนึ่งไปยังอีก file object หนึ่ง
            
        result = collectionVocabulary.insert_one({
            "name": name,
            "read": read,
            "images": img_path,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        vocab_id = str(result.inserted_id)
        
        result_review = collectionVocabularyReview.insert_one({
            "vocab_id": vocab_id,
            "stage": 0,
            "ease_factor": 2.5,
            "review_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        print(f"review inserted: {result_review.inserted_id}")
        return {"id": str(result.inserted_id), "name": name, "read": read, "images": img_path}
    except HTTPException:
        raise
    except Exception as err:
        print(f"ไม่สามารถเพิ่มได้{err}")
        raise HTTPException(status_code=401, detail="เกิดข้อผิดพลาด" )

async def vocabUpdate(vocab_id: str, name: str, read: str, images: UploadFile = None):
    try:
        if not name:
            raise HTTPException(status_code=409, detail="กรุณากรอกชื่อให้เรียบร้อย")
        if not read:
            raise HTTPException(status_code=409, detail="กรุณากรอกคำอ่านให้เรียบร้อย")

        row = collectionVocabulary.find_one({"_id": ObjectId(vocab_id)})
        if not row:
            raise HTTPException(status_code=404, detail="ไม่พบข้อมูล")

        img_path = row.get("images")  # ใช้รูปเดิมก่อน
        # print(f"path ใน DB: {img_path}")
        # print(f"path จริง: {os.path.abspath(img_path)}")
        # print(f"เจอไฟล์ไหม: {os.path.exists(img_path)}")

        if images and images.filename:
            ext = os.path.splitext(images.filename)[1].lower()
            if ext not in ALLOWED_EXT:
                raise HTTPException(status_code=403, detail="ไม่สามารถเพิ่มรูปได้")

            if img_path and os.path.exists(img_path):
                os.remove(img_path) 

            filename = f"{uuid.uuid4()}{ext}"
            img_path = f"{UPLOAD_DIR}{filename}"  # อัพเดท path ใหม่
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            with open(img_path, "wb") as f:
                shutil.copyfileobj(images.file, f)

        collectionVocabulary.update_one(
            {"_id": ObjectId(vocab_id)},
            {"$set": {
                "name": name,
                "read": read,
                "images": img_path,
                "updated_at": datetime.utcnow()
            }}
        )
        return {"_id": vocab_id, "name": name, "read": read, "images": img_path}

    except HTTPException:
        raise
    except Exception as err:
        print(f"เกิดปัญหาระหว่างดำเนินการ {err}")
        raise HTTPException(status_code=500, detail="เกิดข้อผิดพลาด")
    
async def vocbDelete(vocab_id: str):
    try:
        if not vocab_id:
            raise HTTPException(status_code=404, detail="ไอดีไม่ตรง")
        row = collectionVocabulary.find_one({"_id": ObjectId(vocab_id)})
        if not row:
            raise HTTPException(status_code=404, detail="ไม่พบข้อมูล")
        img_path = row.get("images")
        if img_path and os.path.exists(img_path):
            os.remove(img_path)
        collectionVocabulary.delete_one({"_id": ObjectId(vocab_id)})
        collectionVocabularyReview.delete_one({"vocab_id":vocab_id})
        return {"message": "ลบเรียบร้อยแล้ว"}
    except HTTPException:
        raise
    except Exception as err:
        print(f"เกิดปัญหาระหว่างดำเนินการ {err}")
        raise HTTPException(status_code=500, detail="เกิดข้อผิดพลาด")