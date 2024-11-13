from nb.models import User
from nb.program import *

def signupOperation(signupInfo, db):
    signupInfo.accessToken = getAccessToken()
    checkUser = db.query(User).filter(User.username == signupInfo.username).first()
    if checkUser is not None:
        return "User already exists"
    try:
        newUser = User(
            username = signupInfo.username,
            password = signupInfo.password,
            email = signupInfo.email,
            accessToken = signupInfo.accessToken
            
        
        )
        db.add(newUser)
        db.commit()
        return "Registration successful"
    except Exception as error:
        print(error)
        return "Registration Unsuccessful"
    
def loginCheck(loginInfo, db):
    checkUser = db.query(User).filter(User.username == loginInfo.username).first()
    if checkUser is None:
        return "User doesn't exist"
    if checkUser.password == loginInfo.password:
        checkUser.accessToken = getAccessToken()
        try:
            db.commit()
            return f"{checkUser.accessToken}"
        except Exception as error:
            return str(error)
    else:
        return "Wrong password"
    
