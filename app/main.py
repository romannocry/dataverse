from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
import psycopg2
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware


from .models import post,test
from .database import engine
from .routers.posts import router
from .routers.websocket import ws_router
from .routers.tests import router2

#from .config.config import settings

post.Base.metadata.create_all(bind=engine)
test.Base.metadata.create_all(bind=engine)

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
app.include_router(ws_router)
app.include_router(router2)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in ["http://localhost", "http://localhost:5173","http://localhost:5174/"]],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping/")
async def ping(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"message": "pong"}

@app.get("/")
async def root():
    return {"message": "eldorado"}


