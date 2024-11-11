import json
from email.policy import default
from typing import Tuple
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.staticfiles import StaticFiles
from nb.models import Base
import nb.inputSchemas as InSchema
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import nb.handler as HANDLER
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SQLALCHEMY_DATABASE_URL = "sqlite:///./database/agricooo.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def index(request: Request):
    return HANDLER.indexViewer(request)
@app.post("/createAccount")
async def createAccountView(registrationData:InSchema.RegistrationInput, request: Request):
    return HANDLER.createAccountViewer(request, registrationData)


@app.post("/login")
async def loginCheck(loginInfo:InSchema.LoginInfoInput, request : Request):
    return HANDLER.loginChecker(request, loginInfo)
