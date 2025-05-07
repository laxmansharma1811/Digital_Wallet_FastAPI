from pydantic import BaseModel, PositiveFloat
from datetime import datetime


class WalletCreate(BaseModel):
    pass  # No input needed, created automatically for user

class WalletOut(BaseModel):
    id: int
    user_id: int
    balance: float

    class Config:
        from_attributes = True

class DepositRequest(BaseModel):
    amount: PositiveFloat


class TransferRequest(BaseModel):
    target_username: str
    amount: PositiveFloat
    description: str

class TransactionOut(BaseModel):
    id: int
    wallet_id: int
    amount: float
    type: str
    description: str
    created_at: datetime
    target_wallet_id: int | None

    class Config:
        from_attributes = True