from typing import Annotated
from fastapi import Depends, Path, HTTPException, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.testing.pickleable import User
from starlette import status
from models import Todos, Users
from database import SessionLocal
from routers import auth
from passlib.context import CryptContext

router = APIRouter(
    prefix="/user",
    tags = ["user"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(auth.get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserVerification(BaseModel):
    password: str
    new_password: str

@router.get("/user")
async def get_current_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentication Failed")
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verify: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verify.password, user_model.hashed_password):
        raise HTTPException(status_code=400,detail="Incorrect Password")
    user_model.hashed_password = bcrypt_context.hash(user_verify.new_password)
    db.add(user_model)
    db.commit()