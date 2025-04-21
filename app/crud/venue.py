from sqlmodel import Session
from app.models.venue import Venue
from app.schemas.venue import VenueCreate, VenueRead


def create_venue(session: Session, venue_create: VenueCreate) -> VenueRead:
    venue = Venue.from_orm(venue_create)
    session.add(venue)
    session.commit()
    session.refresh(venue)
    return VenueRead.from_orm(venue)
