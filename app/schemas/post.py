from uuid import UUID
from datetime import datetime
from sqlmodel import Field, SQLModel
import uuid

# ✅ Base Model (Not used directly)
class PostBase(SQLModel):
    content: str
    title: str
    published: bool

# ✅ Input Model (for creating posts) → id and created_at are NOT included
class CreatePost(PostBase):
    pass

# ✅ Database Model (for persistence) → id and created_at are auto-generated
class PostDB(PostBase, table=True):  # `table=True` makes it a SQLModel table
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# ✅ Output Model (for responses) → id and created_at are included
class PostOut(PostBase):
    id: UUID
    created_at: datetime