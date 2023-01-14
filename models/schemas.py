from pydantic import BaseModel
from typing import List

class LoginSchema(BaseModel):
    username    : str = 'admin'
    password    : str = 'admin'

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
    family_author       : str
    suborder_id         : int
    
    class Config:
        orm_mode = True
        
        
class FamilySynonymSchema(CategoriesBase):
    family_id           : int
    
    class Config:
        orm_mode = True
        
        
class GenusSchema(CategoriesBase):
    genus_author        : str
    department_id       : int
    class_id            : int
    subclass_id         : int
    supersubclass_id    : int
    order_id            : int
    suborder_id         : int
    family_id           : int
    
    class Config:
        orm_mode = True
        
        
class GenusSynonymSchema(CategoriesBase):
    genus_id            : int
    
    class Config:
        orm_mode = True
    
    

class FullnameSynonymSchema(BaseModel):
    name                : str
    
    class Config:
        orm_mode = True
        
class FullnameSynonymCreateSchema(FullnameSynonymSchema):
    plant_id            : int
    
    class Config:
        orm_mode = True
        
        
class PlantAuthorSchema(BaseModel):
    name                : str
    
    class Config:
        orm_mode = True
        
        
class PlantAuthorCreateSchema(PlantAuthorSchema):
    plant_id            : int
    
    class Config:
        orm_mode = True


class LinkSynonymSchema(BaseModel):
    link                : str
    
    class Config:
        orm_mode = True
        
    
class LinkSynonymCreateSchema(LinkSynonymSchema):
    plant_id            : int
    
    class Config:
        orm_mode = True


class PlantSchema(BaseModel):
    kind                : str
    subkind             : str
    variety             : str
    form                : str
    hybrid              : str
    cultivar            : str
    name_ru             : str
    name_kz             : str
    name_folk           : str
    fullname            : str
    fullname_ru         : str
    department_id       : int
    class_id            : int
    subclass_id         : int
    supersubclass_id    : int
    order_id            : int
    suborder_id         : int
    family_id           : int
    genus_id            : int
    fullname_synonym    : List[FullnameSynonymSchema]
    plant_author        : List[PlantAuthorSchema]
    link_synonym        : List[LinkSynonymSchema]
    
    
    class Config:
        orm_mode = True
        
        
class PlantSchemaUpdate(BaseModel):
    kind                : str
    subkind             : str
    variety             : str
    form                : str
    hybrid              : str
    cultivar            : str
    name_ru             : str
    name_kz             : str
    name_folk           : str
    fullname            : str
    fullname_ru         : str
    department_id       : int
    class_id            : int
    subclass_id         : int
    supersubclass_id    : int
    order_id            : int
    suborder_id         : int
    family_id           : int
    genus_id            : int
    
    class Config:
        orm_mode = True