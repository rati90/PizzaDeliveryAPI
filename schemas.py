from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'username': 'George',
                'email': 'George@sample.com',
                'password': 'password',
                'is_staff': False,
                'is_active': True
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = 'f002cc03812d6514ddaa96e55a094a3ffffebaddd063f3e048514052cdccc353'


class LoginModel(BaseModel):
    username: str
    password: str
