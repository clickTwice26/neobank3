from pydantic import BaseModel


class RegistrationInput(BaseModel):
    username : str
    password : str
    email : str | None = "example@gmail.com"

class LoginInfoInput(BaseModel):
    username : str
    password : str