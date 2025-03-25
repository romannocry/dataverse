from typing import List
from fastapi import (
    HTTPException, 
    Depends, 
    status, 
    APIRouter,
    Body,
    WebSocket,
    WebSocketDisconnect,
    BackgroundTasks
)
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from .. import schemas, models
from app.websockets import manager  # Import the connection manager


router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

async def send_broadcast(message: dict):
    await manager.broadcast(message)

@router.post(
    "/create", 
    status_code=status.HTTP_201_CREATED, 
    response_model=schemas.CreatePost
)
async def create_posts(background_tasks: BackgroundTasks, post: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    background_tasks.add_task(send_broadcast, new_post.content)

    return new_post

@router.get("/{post_id}", response_model=schemas.CreatePost)
def get_post(post_id: UUID, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == str(post_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post  

@router.get("/", response_model=List[schemas.CreatePost])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).limit(1000).all()
    return posts