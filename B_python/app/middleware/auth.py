import jwt
import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException

async def authCheck(credentials: HTTPAuthorizationCredentials = Depends(security)): 
    #Depends(security) class fastapi ดึง token จาก Authorization: Bearer 
    #Depends มีเอาไว้รัน ใน () ก่อนเเล้วเอาผลลัพธ์มา
    #HTTPAuthorizationCredentials type ของข้อมูล HTTPBearer() คืนกลับมา มีแค่ 2 field
    try:
        token = credentials.credentials
        decode = jwt.decode(token, os.getenv("SECRET"), algorithms=["HS256"])
        return decode
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="token หมดอายุ")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="token ไม่ถูกต้อง")
    except Exception as err:
        print(f"ไม่พบข้อมูล: {err}")
        raise HTTPException(status_code=500, detail="เกิดข้อผิดพลาดภายใน")