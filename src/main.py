from fastapi import FastAPI
from routes import base,data

app = FastAPI()   # we use app as decorator 

app.include_router(base.base_router)
app.include_router(data.data_router)
