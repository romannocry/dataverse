from fastapi import FastAPI
import psycopg2

from app import models
from app.database import engine
from .routers.posts import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)

@app.get("/ping/")
async def ping():
    return {"message": "pong"}

@app.get("/")
async def root():
    return {"message": "eldorado"}


