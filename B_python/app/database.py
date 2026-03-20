from pymongo import MongoClient 
import os
try:
    client = MongoClient(os.getenv("MONGO"))
    client.server_info() #chck ให้มันเชื่อต่อจริงไม
    db = client["Reading_Stack"]
    print("Connected to MongoDB")
except Exception as err:
    print("ไม่พบฐานข้อมูล:", err)