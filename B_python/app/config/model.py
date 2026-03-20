from app.database import db
from pydantic import BaseModel ,field_validator,Field
from datetime import datetime
from typing import Optional

collectionUser = db["user"]
collectionVocabulary = db["Vocabulary"]
collectionVocabularyReview = db["Vocabulary_Review"]
collectionArticle = db["Article"]

class User(BaseModel):
    name: Optional[str] =None
    email:str
    password:str
    role:str = "user"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @field_validator("name","email","password")
    def name_not_empty(cls,v):
        if not v.strip():
            raise ValueError("ไม่พบข้อมูล")
        return v.strip()
    
    # password มีไม่เกิน 6
    # @field_validator("password")
    # def password_check(cls, v):
    #     if len(v) < 6:
    #         raise ValueError("รหัสผ่านต้องอย่างน้อย 6 ตัว")
    #     return v
    
    # บอกชื่อ ฟิวด้วย
    # @field_validator("name", "password")
    # def not_empty(cls, v, info: ValidationInfo):
    #     if not v.strip():
    #       raise ValueError(f"{info.field_name} ต้องไม่ว่าง")
    #     return v.strip()

class LoginUser(BaseModel):
    email: str
    password: str

    @field_validator("email", "password")
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError("ไม่พบข้อมูล")
        return v.strip()
    
class Vocabulary(BaseModel):
    name:str
    read:str
    images: str = None # 1 รูป

class Vocabulary_Review(BaseModel):
    vocab_id: str                    # อ้างอิงกลับไป Vocabulary
    stage: int = 0
    ease_factor: float = 2.5
    review_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Article(BaseModel):
    userId:str
    subject:str
    note:str
    images: list[str] = [] # หลายรูป 
    status: str = "draft"
    category: str ="none"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @field_validator("userId","subject","note","category")
    def not_empty(cls, v ,info:ValidationInfo):
        if not v.strip():
            raise ValueError(f"{info.field_name}ไม่ได้กรอกข้อมูล")
        return v.strip()


