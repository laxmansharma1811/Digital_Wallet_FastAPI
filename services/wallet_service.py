from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from models.wallet import Wallet
from models.transaction import Transaction
from resources.wallet import WalletCreate, DepositRequest, TransferRequest
from db.database import get_db
from services.auth_service import get_current_user

def create_wallet(db: Session, user: User = Depends(get_current_user)):
    # Check if user already has a wallet
    existing_wallet = db.query(Wallet).filter(Wallet.user_id == user.id).first()
    if existing_wallet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a wallet",
        )
    
    # Create new wallet
    wallet = Wallet(user_id=user.id, balance=0.0)
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet

def get_wallet(db: Session, user: User = Depends(get_current_user)):
    wallet = db.query(Wallet).filter(Wallet.user_id == user.id).first()
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found",
        )
    return wallet

def deposit_funds(deposit: DepositRequest, db: Session, user: User = Depends(get_current_user)):
    wallet = db.query(Wallet).filter(Wallet.user_id == user.id).first()
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found",
        )
    
    # Update wallet balance
    wallet.balance += deposit.amount
    
    # Record transaction
    transaction = Transaction(
        wallet_id=wallet.id,
        amount=deposit.amount,
        type="deposit",
        description=f"Deposit of {deposit.amount}"
    )
    db.add(transaction)
    db.commit()
    db.refresh(wallet)
    return wallet

def transfer_funds(transfer: TransferRequest, db: Session, user: User = Depends(get_current_user)):
    # Get sender's wallet
    sender_wallet = db.query(Wallet).filter(Wallet.user_id == user.id).first()
    if not sender_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sender wallet not found",
        )
    
    # Get target user and wallet
    target_user = db.query(User).filter(User.username == transfer.target_username).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target user not found",
        )
    
    target_wallet = db.query(Wallet).filter(Wallet.user_id == target_user.id).first()
    if not target_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target wallet not found",
        )
    
    # Check sufficient balance–
    if sender_wallet.balance < transfer.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance",
        )
    
    # Perform transfer (atomic operation)
    try:
        sender_wallet.balance -= transfer.amount
        target_wallet.balance += transfer.amount
        
        # Record sender transaction
        sender_transaction = Transaction(
            wallet_id=sender_wallet.id,
            amount=-transfer.amount,
            type="transfer",
            description=transfer.description,
            target_wallet_id=target_wallet.id
        )
        
        # Record receiver transaction
        receiver_transaction = Transaction(
            wallet_id=target_wallet.id,
            amount=transfer.amount,
            type="transfer",
            description=transfer.description,
            target_wallet_id=sender_wallet.id
        )
        
        db.add(sender_transaction)
        db.add(receiver_transaction)
        db.commit()
        
        db.refresh(sender_wallet)
        return sender_wallet
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Transaction failed",
        )