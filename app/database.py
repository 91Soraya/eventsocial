import os
from sqlmodel import Session, SQLModel, create_engine
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)


# Create the database and tables (if they don´t exist yet)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency


def get_session():
    with Session(engine) as session:
        yield session
