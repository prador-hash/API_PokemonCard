from app.core.settings import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine(Settings.DATABASE_URL)

def get_session():
    with Session(engine, expire_on_commit=False) as session:
        yield session

session = get_session()
