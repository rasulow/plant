from pydantic import BaseModel
from typing import List

class LoginSchema(BaseModel):
    username    : str
    password    : str

    class Config:
        orm_mode = True


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


class ClassSchema(BaseModel):
    name_lt         : str
    name_ru         : str
    department_id   : int
    
    class Config:
        orm_mode = True


class DepartmentSchema(BaseModel):
    name_lt         : str
    name_ru         : str
    class_rel       : List[ClassSchema] = []

    class Config:
        orm_mode = True