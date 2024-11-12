from pydantic import BaseModel
from fastapi import Form


class LoginCheckData(BaseModel):
    username : str
    password : str
    
class SignupData(BaseModel):
    username : str
    password : str
    email : str
    accessToken : str | None = None