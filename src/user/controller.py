
from src.user.dtos import UserSchema
from sqlalchemy.orm import Session

def register(body: UserSchema, db: Session):
    return {"status": "User Registered Successfully.."}