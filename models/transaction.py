from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from db.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # "deposit" or "transfer"
    description = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    target_wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=True)