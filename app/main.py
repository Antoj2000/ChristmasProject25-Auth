from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select

from .database import SessionLocal, engine
from .models import Base, CredentialsDB
from .schemas import TokenRequest, TokenResponse
from .security import verify_password, create_access_token

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # dev-friendly; tighten in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uncomment this line to reset DB
#Base.metadata.drop_all(bind=engine)
#Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/auth/token", response_model=TokenResponse)
def issue_token(payload: TokenRequest, db: Session = Depends(get_db)):
    stmt = select(CredentialsDB).where(
        (CredentialsDB.account_no == payload.account_no)
    )
    cred = db.execute(stmt).scalar_one_or_none()

    if not cred or not verify_password(payload.password, cred.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    token = create_access_token(
        account_id=cred.account_id,
        account_no=cred.account_no,
        email=cred.email,
    )

    return TokenResponse(access_token=token)