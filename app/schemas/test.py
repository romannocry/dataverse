from uuid import UUID
from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column

import uuid

# ✅ Base Model (Not used directly)
class TestBase(SQLModel):
    enrichment: dict = Field(sa_column=Column(JSONB))  # Explicitly use JSONB with Field
    post_id: UUID

    #id: Optional[UUID] = None

# ✅ Input Model (for creating posts) → id and created_at are NOT included
class CreateTest(TestBase):
    pass

# ✅ Database Model (for persistence) → id and created_at are auto-generated
class TestDB(TestBase, table=True):  # `table=True` makes it a SQLModel table
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# ✅ Output Model (for responses) → id and created_at are included
class TestOut(TestBase):
    id: UUID
    created_at: datetime

# Additional properties to return via API
class Test(TestBase):
    id: UUID
    created_at: datetime
