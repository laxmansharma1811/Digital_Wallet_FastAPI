from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine
from models.user import Base
from controller.auth_controller import router as auth_router
from controller.wallet_controller import router as wallet_router

# Initialize FastAPI app
app = FastAPI(title="Digital Wallet API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include authentication routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(wallet_router, prefix="/wallet", tags=["Wallet"])

@app.get("/")
def read_root():
    return {"message": "Digital Wallet API"}