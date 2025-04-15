import os
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)


# Define the Venue model
class Venue(SQLModel, table=True):
    __tablename__ = "venues"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    address: str = Field(index=True)
    city: str = Field(index=True)
    country: str = Field(index=True)
    created_at: datetime | None = Field(default=None)


# Create the database and tables (if they don´t exist yet)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

# Create FastAPI app
app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/venues/")
def create_venue(venue: Venue, session: SessionDep) -> Venue:
    session.add(venue)
    session.commit()
    session.refresh(venue)
    return venue


@app.get("/venues/")
def read_venues(
        session: SessionDep,
        offset: int=0,
        limit: Annotated[int, Query(le=100)] = 100,
) -> list[Venue]:
    venues = session.exec(select(Venue).offset(offset).limit(limit)).all()
    return venues


@app.get("/venues/{venue_id}")
def read_venue(venue_id: int, session: SessionDep) -> Venue:
    venue = session.get(Venue, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue


@app.delete("/venues/{venue_id}")
def delete_venue(venue_id: int, session: SessionDep):
    venue = session.get(Venue, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    session.delete(venue)
    session.commit()
    return {"ok": True}
