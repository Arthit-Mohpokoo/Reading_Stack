import shutil , uuid,os
from app.config.model import collectionArticle
from bson import ObjectId
from datetime import datetime
from fastapi import UploadFile, File, Form, HTTPException

ALLOWED_EXT = {".png", ".jpg", ".jpeg", ".webp"}
UPLOAD_DIR = "app/upload/Article/"

async def ArticleCreate(
    userId: str,
    subject: str,
    note: str,
    images: list[UploadFile]=[],
    status: str = "draft",
    category: str = "none"
):
    try:
        if not subject:
            raise HTTPException(status_code=409, detail="กรุณากรอกชื่อให้เรียบร้อย")
        
        img_paths = []
        for image in images:
            if image and image.filename:
                pimg = os.path.splitext(image.filename)[1].lower()
                
                if pimg not in ALLOWED_EXT:
                    raise HTTPException(status_code=403, detail="ไม่สามารถเพิ่มรูปได้")
                filename = f"{uuid.uuid4()}{pimg}" 
                img_path = f"{UPLOAD_DIR}{filename}"
                
                with open(img_path, "wb") as f:
                    shutil.copyfileobj(image.file, f)
                img_paths.append(img_path)
                
        result = collectionArticle.insert_one({
            "userId": userId,
            "subject": subject,
            "note": note,
            "images": img_paths,
            "status": status,
            "category": category,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        return {"id": str(result.inserted_id), "subject": subject, "status": status, "category": category}
    except HTTPException:
        raise
    except Exception as err:
        print(f"ไม่สามารถเพิ่มได้ {err}")
        raise HTTPException(status_code=401, detail="เกิดข้อผิดพลาด" )

async def ArticleUpdate(article_id: str, subject: str, note: str,
    images: list[UploadFile] = [], status: str = "draft", category: str = "none"):
    try:
        if not subject:
            raise HTTPException(status_code=409, detail="กรุณากรอกชื่อให้เรียบร้อย")

        row = collectionArticle.find_one({"_id": ObjectId(article_id)})
        if not row:
            raise HTTPException(status_code=404, detail="ไม่พบข้อมูล")

        img_paths = row.get("images", [])  # ใช้รูปเดิมก่อน

        if images:
            # ลบรูปเก่าทั้งหมด
            for old_path in img_paths:
                if old_path and os.path.exists(old_path):
                    os.remove(old_path)
            img_paths = []  # reset list

            # save รูปใหม่
            for image in images:
                if image and image.filename:
                    pimg = os.path.splitext(image.filename)[1].lower()
                    if pimg not in ALLOWED_EXT:
                        raise HTTPException(status_code=403, detail="ไม่สามารถเพิ่มรูปได้")
                    filename = f"{uuid.uuid4()}{pimg}"
                    img_path = f"{UPLOAD_DIR}{filename}"
                    os.makedirs(UPLOAD_DIR, exist_ok=True)
                    with open(img_path, "wb") as f:
                        shutil.copyfileobj(image.file, f)
                    img_paths.append(img_path)

        collectionArticle.update_one(
            {"_id": ObjectId(article_id)},
            {"$set": {
                "subject": subject,
                "note": note,
                "images": img_paths,  # ✓ list
                "status": status,
                "category": category,
                "updated_at": datetime.utcnow()
            }}
        )
        return {"message": "แก้ไขเรียบร้อย"}
    except HTTPException:
        raise
    except Exception as err:
        print(f"ไม่สามารถแก้ไขได้: {err}")
        raise HTTPException(status_code=500, detail="เกิดข้อผิดพลาด")
    
    
async def ArticleDelete(article_id:str):
    try:
        if not article_id:
            raise HTTPException(status_code=404, detail="ไอดีไม่ตรง")
        
        row = collectionArticle.find_one({"_id": ObjectId(article_id)})
        if not row:
            raise HTTPException(status_code=404, detail="ไม่พบข้อมูล")
        
        img_paths = row.get("images", [])
        for img_path in img_paths:
            # print(f"กำลังลบ: {img_path}")
            if img_path and os.path.exists(img_path):
                os.remove(img_path)
        collectionArticle.delete_one({"_id":ObjectId(article_id)})
        return {"message": "ลบเรียบร้อยแล้ว"}
    except HTTPException:
        raise
    except Exception as err:
        print(f"ไม่สามารถเพิ่มได้ {err}")
        raise HTTPException(status_code=401, detail="เกิดข้อผิดพลาด" )

async def ArticleDeleteOneImg(article_id: str, img_index: int):
    try:
        row = collectionArticle.find_one({"_id": ObjectId(article_id)})
        if not row:
            raise HTTPException(status_code=404, detail="ไม่พบข้อมูล")

        img_paths = row.get("images", [])

        if img_index < 0 or img_index >= len(img_paths):
            raise HTTPException(status_code=404, detail="ไม่พบรูปที่ต้องการลบ")

        img_to_delete = img_paths[img_index] 

        if img_to_delete and os.path.exists(img_to_delete):
            os.remove(img_to_delete)

        img_paths.pop(img_index)

        collectionArticle.update_one(
            {"_id": ObjectId(article_id)},
            {"$set": {"images": img_paths}}
        )
        return {"message": "ลบรูปเรียบร้อย", "images": img_paths}
    except HTTPException:
        raise
    except Exception as err:
        print(f"ไม่สามารถลบรูปได้: {err}")
        raise HTTPException(status_code=500, detail="เกิดข้อผิดพลาด")