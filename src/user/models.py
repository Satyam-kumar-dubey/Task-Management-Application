
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.utils.db import Base

class UserModel(Base):
    __tablename__ = "users_table"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String)
    hash_password = Column(String, nullable=False)
    
    