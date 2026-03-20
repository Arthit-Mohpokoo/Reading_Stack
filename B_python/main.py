from fastapi import FastAPI
from app.routes.auth import routes
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import importlib

app=FastAPI(title= "Reading FAST API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

route_path = Path(__file__).parent / "app" / "routes"

for file in route_path.glob("*.py"):
    if file.name == "__init__.py":
        continue
    module_name = file.stem #ย่อมาจากชื่อไฟล์
    module = importlib.import_module(f"app.routes.{module_name}") #pathที่มา
    # print(f"app.routes.{module_name}") # check path api
    
    if hasattr(module , "routes"):
        app.include_router(module.routes, prefix="/api")

