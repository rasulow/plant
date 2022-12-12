from pydantic import BaseModel
from typing import List

class AdminBase(BaseModel):
    user_type       : str = 'user'
    username        : str
    password        : str
    is_active       : bool = False
    is_superadmin   : bool = False

    class Config:
        orm_mode = True


class AdminDelete(BaseModel):
    user_type       : str = 'user'
    is_deleted      : bool = True

    class Config:
        orm_mode = True


class AdminActiveSet(BaseModel):
    user_type       : str = 'user'
    is_active       : bool = True

    class Config:
        orm_mode = True
