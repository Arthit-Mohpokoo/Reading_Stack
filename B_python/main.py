from fastapi import FastAPI , HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from bson.objectid import ObjectId

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["Reading_Stack"]
collection = db["user"]

class User(BaseModel):
    name:str
    count:int

@app.get("/")
async def root():
    return {"meassage":"hello world"}

# @app.post("/user")
# async def create_user(loguser:User):
#     result = collection.insert_one(loguser.dict())
#     return{
#         "id" : str(result.inserted_id),
#         "name": loguser.name,
#         "count" : loguser.count
#     }
    
# @app.get("/user/{user_id}")
# async def read_user(user_id:str):
#     iduser = collection.find_one({"_id": ObjectId(user_id)})
#     if iduser :
#         return{"id": str(iduser["_id"]),"name": iduser["name"],"count": iduser["count"]}
#     else:
#         raise HTTPException(status_code=404, detail="iduser not found")