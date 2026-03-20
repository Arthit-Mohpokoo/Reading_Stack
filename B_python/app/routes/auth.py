from fastapi import APIRouter
from app.controller.auth import register,login
from app.config.model import User,LoginUser

routes = APIRouter()

@routes.post('/register')
async def root(user:User):
    return await register(user)

@routes.post('/login')
async def root(user:LoginUser):
    return await login(user)