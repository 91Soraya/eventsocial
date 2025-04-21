from fastapi import FastAPI
from app.database import engine
from app.models.venue import Venue
from app.routers.venue import venue_router


# Create FastAPI app
app = FastAPI()


@app.on_event("startup")
def on_startup():
    Venue.metadata.create_all(engine)


app.include_router(venue_router)


"""
@app.post("/venues/")
def create_venue(venue: models.Venue, session: SessionDep) -> models.Venue:
    session.add(venue)
    session.commit()
    session.refresh(venue)
    return venue


@app.get("/venues/")
def read_venues(
        session: SessionDep,
        offset: int=0,
        limit: Annotated[int, Query(le=100)] = 100,
) -> list[models.Venue]:
    venues = session.exec(select(models.Venue).offset(offset).limit(limit)).all()
    return venues


@app.get("/venues/{venue_id}")
def read_venue(venue_id: int, session: SessionDep) -> models.Venue:
    venue = session.get(models.Venue, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue


@app.delete("/venues/{venue_id}")
def delete_venue(venue_id: int, session: SessionDep):
    venue = session.get(models.Venue, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    session.delete(venue)
    session.commit()
    return {"ok": True}
"""