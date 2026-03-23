from fastapi import APIRouter, UploadFile, File, Form
from app.controller.Vocabulary import vocabC,vocabUpdate,vocbDelete
from app.config.model import Vocabulary


routes= APIRouter()

@routes.post("/vocabulary")
async def root(
    userid: str = Form(...),
    name: str = Form(...),
    read: str = Form(...),
    images: UploadFile = File(None)
):
    try:
        return await _create_vocab(userid, name, read, images) 
    except HTTPException:
        raise
    except Exception as err:
        raise HTTPException(status_code=500, detail="เกิดข้อผิดพลาด")

@routes.put("/vocabulary/{vocab_id}")
async def root(
    
    name: str = Form(...),
    read: str = Form(...),
    images: UploadFile = File(None)
):
    return await vocabUpdate(vocab_id,name,read,images)

@routes.delete("/vocabularyD/{vocab_id}")
async def root(
    vocab_id: str):
    return await vocbDelete(vocab_id)