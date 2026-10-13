
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from src.utils.settings import setting

Base = declarative_base()
Engine = create_engine(url=setting.DB_CONNECTION)

SessionLocal = sessionmaker(bind=Engine)

def get_db():
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.close()