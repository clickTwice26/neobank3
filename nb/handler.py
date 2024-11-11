from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


def createAccountViewer(request, regInfo):
    print(f"{regInfo.username}")
    return "Hello I got the response"


def indexViewer(request):
    return templates.TemplateResponse("index.html", {"request": request})

def loginChecker(request, loginInfo):
    if loginInfo.username == "test" and loginInfo.password == "test":
        return "Success"
    else:
        return "Wrong username or password"