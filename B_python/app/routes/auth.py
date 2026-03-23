from fastapi import APIRouter,Depends
from app.controller.auth import register,login,conuser
from app.config.model import User,LoginUser
from app.middleware.auth import authCheck

routes = APIRouter()

@routes.post('/register')
async def root(user:User):
    return await register(user)

@routes.post('/login')
async def root(user:LoginUser):
    return await login(user)

@routes.get('/curren-user')
async def root(user = Depends(authCheck)):
    return await conuser(user)