from datetime import datetime,timedelta
from fastapi import HTTPException, status, Request
from src.user.dtos import UserSchema, loginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from src.utils.settings import setting
from src.utils.mail import send_email

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

async def register(body: UserSchema, db: Session):
    
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    
    if is_user:
        raise HTTPException(400, detail="User Already Exists..")
    
    is_userEmail = db.query(UserModel).filter(UserModel.email == body.email).first()
    
    if is_userEmail:
        raise HTTPException(400, detail="Email Address already Exists..")
    
    hash_password = get_password_hash(body.password)
    
    new_user =  UserModel(
        name = body.name,
        username = body.username,
        email = body.email,
        hash_password = hash_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    ##sending the confirmation email 
    
    res = await send_email([new_user.email])
    
    return new_user


def login(body : loginSchema, db : Session):
    
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You Have Entered Wrong Username!")
    
    if not verify_password(body.password, user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You have Entered Wrong Password!")
    
    
    exp_time = datetime.now() + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"_id":user.id, "exp": exp_time.timestamp()},setting.SECRET_KEY,setting.ALGORITHM)
    
    return {"token": token}


def is_authenticated(request:Request, db:Session):

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
    