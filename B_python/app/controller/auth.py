from app.config.model import collectionUser , User,LoginUser
from fastapi import HTTPException
import os
import bcrypt
import jwt
from dotenv import load_dotenv
load_dotenv()
async def register(user:User):
    try:
        email = user.email.lower()
        existing = collectionUser.find_one({"email": user.email})
        if existing:
            raise HTTPException(status_code=409, detail="อีเมลนี้มีอยู่แล้ว")
        
        hashed = bcrypt.hashpw(user.password.encode("utf-8"),bcrypt.gensalt(10)) 
        data = user.model_dump()
        data["email"] = email
        data["password"] = hashed.decode("utf-8") #ทำให้เป็นสตริงก่อนเก็บ .ecode("utf-8")
        
        result = collectionUser.insert_one(data) #dict ไม่รองรับ await
        return {
            "id": str(result.inserted_id),
            "email": user.email
        }
    except HTTPException:
        raise
    except Exception as err :
        print(f"ไม่สามารถสร้างได้ : {err}")
        raise HTTPException(status_code=500, detail="เกิดข้อผิดพลาดภายใน")

async def login (user:LoginUser):
    try:
        print("SECRET =", os.getenv("SECRET"))
        checkuser = collectionUser.find_one({"email":user.email.lower()})
        if not checkuser :
             raise HTTPException(status_code=409, detail="ไม่พบบัญชีนี้ในระบบ")

        is_match = bcrypt.checkpw(
            str(user.password).encode("utf-8"),
            checkuser["password"].encode("utf-8")
        )
        
        if not is_match:
            raise HTTPException(status_code=401, detail="รหัสผ่านไม่ถูกต้อง")
        
        payload ={
            "id": str(checkuser["_id"]),
            "email":checkuser["email"],
            "role" : checkuser["role"]
        }
        token = jwt.encode(payload, os.getenv("SECRET"), algorithm="HS256")
        # encode = jwt.encode({payload},"secret", algorithm="HS256") #อันเก่าที่ผิดพลาด
        
        return {
            "id": str(checkuser["_id"]),
            "email": checkuser["email"],
            "message": "เข้าสู่ระบบสำเร็จ",
            "token": token
        }
    except HTTPException:
        raise
    except Exception as err:
        print(f"เกิดข้อผิดพลาด: {err}")
        raise HTTPException(status_code=500, detail="เกิดข้อผิดพลาดภายใน")