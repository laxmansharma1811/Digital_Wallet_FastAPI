from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from resources.wallet import WalletCreate, WalletOut, DepositRequest, TransferRequest
from services.wallet_service import create_wallet, get_wallet, deposit_funds, transfer_funds
from models.user import User
from services.auth_service import get_current_user
from db.database import get_db

router = APIRouter()

@router.post("/create", response_model=WalletOut)
def create_user_wallet(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_wallet(db, user)

@router.get("/", response_model=WalletOut)
def get_user_wallet(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_wallet(db, user)

@router.post("/deposit", response_model=WalletOut)
def deposit_to_wallet(deposit: DepositRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return deposit_funds(deposit, db, user)

@router.post("/transfer", response_model=WalletOut)
def transfer_to_wallet(transfer: TransferRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return transfer_funds(transfer, db, user)