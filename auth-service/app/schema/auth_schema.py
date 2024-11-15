from pydantic import BaseModel


class SignUp(BaseModel):
    login: str
    password: str


class SignIn(BaseModel):
    login: str
    password: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class Token(BaseModel):
    access_token: str
    user_id: int
