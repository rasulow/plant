from pydantic import BaseModel
from typing import List
import json

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
    name_tm         : str


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
        
        
class ArealSchema(BaseModel):
    floristic_regions       : str
    abbreviated_names       : str
    old_names               : str
    study_territory         : str
    administrative_regions  : str
    geographic_regions      : str
    additional_areals       : str
    general_distribution    : str
    geo_groups_areals       : str
    plant_id                : int
    
    class Config:
        orm_mode = True
        
        
class MorphologySchema(BaseModel):
    growth_form                     : str
    deciduousness                   : str
    life_form_raunkier              : str
    fruit_bearing                   : str
    type_pollination                : str
    begin_flowering_decade          : str
    begin_flowering_month           : str
    end_flowering_decade            : str
    end_flowering_month             : str
    fruit_ripening_decade           : str
    fruit_ripening_month            : str
    flower_color_shade              : str
    flower_color_background         : str
    fruit_color_shade               : str
    fruit_color_background          : str
    leaf_color_summer_shade         : str
    leaf_color_summer_background    : str
    leaf_color_autumn_shade         : str
    leaf_color_autumn_background    : str
    description_structure           : str
    additional                      : str
    plant_id                        : int
    
    class Config:
        orm_mode = True
        
        
class EcologySchema(BaseModel):
    natural_area            : str
    vegetation_type         : str
    vegetation_subtype      : str
    habitats                : str
    phytoprotective_status  : str
    endemicity              : str
    relic                   : str
    aboriginality           : str
    water                   : str
    soil_fertility          : str
    soil_salinity           : str
    light                   : str
    other_features          : str
    plant_id                : int
    
    class Config:
        orm_mode = True
        
        
class NoteSchema(BaseModel):
    text                    : str
    plant_id                : int
    
    class Config:
        orm_mode = True
        
        
class ApplySchema(BaseModel):
    can_be_used1            : str
    can_be_used2            : str
    can_be_used3            : str
    as_decorative1          : str
    as_decorative2          : str
    while_creating          : str
    for_phytomelioration1   : str
    for_phytomelioration2   : str
    for_phytomelioration3   : str
    as_food                 : str
    as_feed                 : str
    as_medicinal            : str
    as_technical            : str
    for_other_purposes      : str
    availability_materials  : str
    propagated_seeds        : str
    propagated_vegetatively : str
    propagated_condition    : str
    main_ways_prop          : str
    plant_id                : int
    
    class Config:
        orm_mode = True
        
        

class AdditionSchema(BaseModel):
    red_book1           : str
    red_book2           : str
    red_book3           : str
    source1             : str
    source2             : str
    source3             : str
    source4             : str
    source5             : str
    note                : str
    botanical_institute : str
    performer_position  : str
    performer_degree    : str
    performer_fullname  : str
    plant_id            : int
    
    class Config:
        orm_mode = True
        
        
class HerbariumSchema(BaseModel):
    date_of_selection   : str
    region              : str
    area                : str
    place_of_selection  : str
    geo_latitude        : str
    geo_longitude       : str
    sea_level           : str
    plant_id            : int

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    class Config:
        orm_mode = True