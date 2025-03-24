from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
import psycopg2
from typing import Annotated


from .models import post
from .database import engine
from .routers.posts import router
#from .config.config import settings

post.Base.metadata.create_all(bind=engine)
init_oauth = {
    "clientId": "facObec-936a-446-9500-44f0d935f462",
    "scopes": "openid profile",
    "additionalQueryStringParams":{
        "nonce":"SWAGGER"
    }
}

#app = FastAPI()
#app = FastAPI(
#    swagger_ui_init_oauth=init_oauth,title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
#)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(router)

@app.get("/ping/")
async def ping(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"message": "pong"}

@app.get("/")
async def root():
    return {"message": "eldorado"}


