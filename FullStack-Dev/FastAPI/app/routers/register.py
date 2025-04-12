from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from passlib.context import CryptContext

from app.models.models import User, Role
from app.database.database import get_db
from app.models.schemas import UserCreate

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # get DEFAULT role when new user is registered! 
    # (default -> customer or select type of user: Seller or Customer)
    role = db.query(Role).filter(Role.name == "user").first()
    new_user = User(username=user.username, 
                    hashed_password=get_password_hash(user.password), 
                    role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username}