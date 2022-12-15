from pydantic import BaseModel
from typing import List

class AdminBase(BaseModel):
    username        : str
    password        : str
    is_active       : bool = False
    is_superadmin   : bool = False

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username        : str
    password        : str
    is_active       : bool = False

    class Config:
        orm_mode = True


class UserDelete(BaseModel):
    is_deleted      : bool = True

    class Config:
        orm_mode = True


class UserActiveSet(BaseModel):
    is_active       : bool = True

    class Config:
        orm_mode = True