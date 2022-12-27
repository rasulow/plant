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


class DeleteSchema(BaseModel):
    is_deleted      : bool

    class Config:
        orm_mode = True


class CategoriesBase(BaseModel):
    name_lt         : str
    name_ru         : str


class DepartmentSchema(CategoriesBase):
    pass

    class Config:
        orm_mode = True


class ClassSchema(CategoriesBase):
    department_id   : int
    
    class Config:
        orm_mode = True
        

class SubclassSchema(CategoriesBase):
    department_id   : int
    class_id        : int
    
    class Config:
        orm_mode = True


class SupersubclassSchema(CategoriesBase):
    department_id   : int
    class_id        : int
    subclass_id     : int
    
    class Config:
        orm_mode = True



class OrderSchema(CategoriesBase):
    department_id       : int
    class_id            : int
    subclass_id         : int
    supersubclass_id    : int
    
    class Config:
        orm_mode = True


class SuborderSchema(CategoriesBase):
    department_id       : int
    class_id            : int
    subclass_id         : int
    supersubclass_id    : int
    order_id            : int
    
    class Config:
        orm_mode = True