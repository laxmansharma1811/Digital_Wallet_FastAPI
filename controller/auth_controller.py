from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from resources.user import UserCreate, UserLogin, Token, UserOut
from services.auth_service import create_user, authenticate_user, create_access_token, get_current_user
from db.database import get_db
from models.user import User

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.post("/login", response_model=Token)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user)
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile", response_model=UserOut)
async def get_current_user(token: str, db : Session = Depends(get_db)):
    db_user = await get_current_user(token, db)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return db_user