from sqlalchemy import (
    Column, 
    Integer, 
    UUID,
    String, 
    Boolean, 
    TIMESTAMP, 
    text
)
from sqlalchemy import DateTime, func
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

import uuid

from pydantic import EmailStr


from app.database import Base

class Test(Base):
    __tablename__ = "tests"

    id =  Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID)
    enrichment: dict = Column(JSONB)  # Use the JSONB column directly
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    #created_at =datetime.now()
    #created_at= Column(
    #        DateTime(timezone=True), server_default=func.now(), nullable=True
    #    )