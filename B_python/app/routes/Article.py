from fastapi import APIRouter, UploadFile ,File,Form
from app.controller.Article import ArticleCreate,ArticleDelete,ArticleUpdate ,ArticleDeleteOneImg

routes = APIRouter()

@routes.post("/Article")
async def root(
    userId: str = Form(...),
    subject: str = Form(...),
    note: str = Form(...),
    images: list[UploadFile]=File([]),
    status: str = Form("draft"),
    category: str = Form("none")
):
    return await ArticleCreate(userId, subject, note, images, status, category)

@routes.put("/ArticleUpdate/{article_id}")
async def root(
    article_id:str,
    subject: str = Form(...),
    note: str = Form(...),
    images: list[UploadFile]=File([]),
    status: str = Form("draft"),
    category: str = Form("none")
):
    return await ArticleUpdate(article_id, subject, note, images, status, category)

@routes.delete("/ArticleDelete/{article_id}")
async def root(article_id:str):
    return await ArticleDelete(article_id)
@routes.delete("/Article/{article_id}/image/{img_index}")
async def root(article_id: str, img_index: int):
    return await ArticleDeleteOneImg(article_id, img_index)