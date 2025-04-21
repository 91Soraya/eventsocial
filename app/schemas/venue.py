from datetime import datetime
from pydantic import BaseModel


class VenueCreate(BaseModel):
    name: str
    address: str
    city: str
    country: str


class VenueRead(VenueCreate):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
