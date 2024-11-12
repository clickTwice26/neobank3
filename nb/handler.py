from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from nb.forms import LoginForm, SignupForm
from nb.models import User
from nb.program import *
templates = Jinja2Templates(directory="templates")




def indexViewer(request):
    return templates.TemplateResponse("index.html", {"request": request})

def loginChecker(request, loginInfo):
    if loginInfo.username == "test" and loginInfo.password == "test":
        return "Success"
    else:
        return "Wrong username or password"
    
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

    