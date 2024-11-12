import json
from email.policy import default
from typing import Tuple
from fastapi import FastAPI, Depends, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.staticfiles import StaticFiles
from nb.models import Base
import nb.inputSchemas as InSchema
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import nb.handler as HANDLER
from nb.forms import SignupForm
import nb.apihandler as API_HANDLER
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

SQLALCHEMY_DATABASE_URL = "sqlite:///./database/neobank3.db"
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
#, db: Session = Depends(get_db)
@app.get("/login")
async def loginPage(request : Request):
    return HANDLER.loginViewer(request)
@app.get("/signup")
async def signupPage(request : Request):
    return HANDLER.signupViewer(request)



@app.post("/login/check")
async def loginCheck(request : Request, db : Session = Depends(get_db)):
    return HANDLER.loginChecker()


@app.post("/signup/check")
async def signupOperation(request: Request, db : Session = Depends(get_db), username : str = Form(...), password : str = Form(...), email :str = Form(...)):
    registrationData = InSchema.SignupData(username=username, password=password, email=email)
    return HANDLER.signupOperator(request, db, registrationData)


@app.post("/api/login")
async def loginCheck(loginInfo:InSchema.LoginCheckData, request : Request, db: Session = Depends(get_db)):
    return API_HANDLER.loginCheck(loginInfo, db)

@app.post("/api/signup")
async def API_signup(signupInfo : InSchema.SignupData, db : Session = Depends(get_db)):
    return API_HANDLER.signupOperation(signupInfo, db)

