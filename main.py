from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv(".env")
from routes import base

app = FastAPI()   # we use app as decorator 

app.include_router(base.base_router)
