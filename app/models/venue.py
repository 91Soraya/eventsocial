from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Venue(SQLModel, table=True):
    __tablename__ = "venues"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    address: str = Field(index=True)
    city: str = Field(index=True)
    country: str = Field(index=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
