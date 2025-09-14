from pydantic import BaseModel, Field
from datetime import datetime, timezone

class Habit(BaseModel):
    id: int
    name: str
    color: str = Field(default="#22c55e")
    cadence: str = Field(default="daily")
    created_at: datetime = Field(default=datetime.now(timezone.utc))
    owner_id: int = Field(foreign_key="users.id", ondelete="CASCADE")