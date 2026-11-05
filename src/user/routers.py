
from fastapi import APIRouter, Depends, status, Request
from src.user.dtos import UserSchema, UserResponseSchema, loginSchema
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user import controller

user_routes = APIRouter(prefix="/users")

@user_routes.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register(body: UserSchema, db : Session = Depends(get_db)):
    return await controller.register(body,db)


@user_routes.post("/login", status_code=status.HTTP_200_OK)
def login(body:loginSchema, db : Session = (Depends(get_db))):
    return controller.login(body,db)


@user_routes.get("/auth", status_code=status.HTTP_200_OK, response_model= UserResponseSchema)
def authenticated(request:Request, db:Session = Depends(get_db)):
    return controller.is_authenticated(request,db)