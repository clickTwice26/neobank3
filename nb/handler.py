from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from nb.forms import LoginForm, SignupForm
from nb.models import User
from fastapi import Request
import typing
from nb.program import *
templates = Jinja2Templates(directory="templates")

def flash(request: Request, message: typing.Any, category: str = "primary") -> None:
   if "_messages" not in request.session:
       request.session["_messages"] = []
       request.session["_messages"].append({"message": message, "category": category})
def get_flashed_messages(request: Request):
   print(request.session)
   return request.session.pop("_messages") if "_messages" in request.session else []

templates.env.globals["get_flashed_messages"] = get_flashed_messages

def indexViewer(request):
    return templates.TemplateResponse("index.html", {"request": request})

def loginChecker(request, loginInfo, db):
    checkUser = db.query(User).filter(User.username == loginInfo.username).first()
    if checkUser is None:
        return "Wrong Username or Passsord"
    if checkUser.password == loginInfo.password:
        
        if createSession(request, loginInfo.username, db):
            flash(request, "Login Successful", "success")
            print(request.session)
            return RedirectResponse("/", status_code=303)
        
    else:
        flash(request, "Login Failed", "success")
        return RedirectResponse("/", status_code=303)
        
def loginViewer(request):
    form = LoginForm(request)
    return templates.TemplateResponse("login.html", {"request" : request, "form": form})

def signupViewer(request):
    form = SignupForm(request)
    return templates.TemplateResponse("signup.html", {"request": request, "form" : form})

def signupOperator(request, db, signupData):
    
    userList = db.query(User).filter(User.username == signupData.username).first()
    if userList is None:
        print("DEBUG", signupData.username, signupData.email)
        signupData.accessToken = getAccessToken()
        newUser = User(
            **signupData.model_dump()
        )
        db.add(newUser)
        db.commit()
        return "registration completed"
    else:
        return "User already exist"

def createSession(request, username, db): # Not HANDLER
    try:
        userData = db.query(User).filter(User.username == username).first()        
        request.session['accessToken'] = userData.accessToken
        request.session['username'] = userData.username
        return True
    except Exception as error:
        return False
    
def verify(request, db): # Not HANDLER 
    try:
        checkUser = db.query(User).filter(User.username == request.session.get('username')).first()
        if checkUser is None:
            return False
        else:
            if checkUser.accessToken == request.session.get("accessToken"):
                return True
            else:
                request.session.clear()
                return False
    except Exception as error:
        return False
def Developer(request, db):
    userlist = db.query(User).filter().all()
    return templates.TemplateResponse("test.html", {"request" : request, "userlist": userlist})
class Userinfo:
    def __init__(self, username, db):
        self.userData = db.query(User).filter(User.username == username).first()