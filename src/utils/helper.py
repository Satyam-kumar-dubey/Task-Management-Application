

from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
from src.utils.settings import setting
from src.user.models import UserModel
from src.utils.db import get_db



def is_authenticated(request:Request, db:Session = Depends(get_db)):

    try:
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are Unauthorized")
        token = token.split(" ")[-1]
        
        data = jwt.decode(token, setting.SECRET_KEY, setting.ALGORITHM)
        user_id = data.get("_id")
        
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are Unauthorized")
        
    
        return user
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are Unauthorized")
    