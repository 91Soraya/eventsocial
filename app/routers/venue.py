from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.schemas.venue import VenueCreate, VenueRead
from app.crud.venue import create_venue
from app.models.venue import Venue
from typing import List

venue_router = APIRouter(prefix="/venues", tags=["Venues"])


# POST
@venue_router.post("/", response_model=VenueRead)
def create_venue_route(venue: VenueCreate, session: Session = Depends(get_session)):
    return create_venue(session=session, venue_create=venue)


# GET all venues
@venue_router.get("/", response_model=List[VenueRead])
def read_venues(session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100)):
    venues = session.exec(select(Venue).offset(offset).limit(limit)).all()
    return venues


# GET a single venue by UUID
@venue_router.get("/{venue_id}", response_model=VenueRead)
def read_venue(venue_id: int, session: Session = Depends(get_session)):
    venue = session.get(Venue, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue


# DELETE a venue
@venue_router.delete("/{venue_id}")
def delete_venue(venue_id: int, session: Session = Depends(get_session)):
    venue = session.get(Venue, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    session.delete(venue)
    session.commit()
    return {"ok": True}
