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
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

router2 = APIRouter(
    prefix="/tests",
    tags=["tests"]
)

async def send_broadcast(message: dict):
    await manager.broadcast(message)

@router2.post(
    "/create", 
    status_code=status.HTTP_201_CREATED, 
    response_model=schemas.CreateTest
)
async def create_tests(post: schemas.CreateTest, db: Session = Depends(get_db)):
    try:
        new_test = models.Test(**post.dict())
        db.add(new_test)
        db.commit()
        db.refresh(new_test)
        
        return new_test

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Database error. Please try again later.",
        )

@router2.get("/{test_id}", response_model=schemas.CreateTest)
def get_post(test_id: UUID, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.test.id == str(test_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post  

@router2.get("/", response_model=List[schemas.Test])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Test).limit(1000).all()
    return posts