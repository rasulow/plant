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

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username        : str
    password        : str

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


class ClassSchema(DepartmentSchema):
    department_id   : int
    
    class Config:
        orm_mode = True
        

class SubclassSchema(ClassSchema):
    class_id        : int
    
    class Config:
        orm_mode = True


class SupersubclassSchema(SubclassSchema):
    subclass_id     : int
    
    class Config:
        orm_mode = True



class OrderSchema(SupersubclassSchema):
    supersubclass_id    : int
    
    class Config:
        orm_mode = True


class SuborderSchema(OrderSchema):
    order_id            : int
    
    class Config:
        orm_mode = True
        
        
class FamilySchema(SuborderSchema):
    suborder_id         : int
    
    class Config:
        orm_mode = True