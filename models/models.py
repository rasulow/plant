from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean, ForeignKey, Date, Time
from datetime import datetime
from sqlalchemy.orm import relationship
from db import Base


# authentication model
class Users(Base):
    __tablename__   = 'users'
    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String)
    password        = Column(String)
    token           = Column(String)
    is_active       = Column(Boolean, default=True)
    is_deleted      = Column(Boolean, default=False)
    create_at       = Column(DateTime, default=datetime.now)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Admin(Base):
    __tablename__   = 'admin'
    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String)
    password        = Column(String)
    token           = Column(String)
    is_superadmin   = Column(Boolean, default=False)
    is_active       = Column(Boolean, default=False)
    is_deleted      = Column(Boolean, default=False)
    create_at       = Column(DateTime, default=datetime.now)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Department(Base):
    __tablename__   = 'department'
    id              = Column(Integer, primary_key=True, index=True)
    name_lt         = Column(String)
    name_ru         = Column(String)
    name_tm         = Column(String)
    is_deleted      = Column(Boolean, default=False)
    create_at       = Column(DateTime, default=datetime.now)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    class_rel       = relationship('Class'          , cascade="all,delete", back_populates='department')
    subclass        = relationship('Subclass'       , cascade="all,delete", back_populates='department')
    supersubclass   = relationship('Supersubclass'  , cascade="all,delete", back_populates='department')
    order           = relationship('Order'          , cascade="all,delete", back_populates='department')
    suborder        = relationship('Suborder'       , cascade="all,delete", back_populates='department')
    family          = relationship('Family'         , cascade="all,delete", back_populates='department')
    genus           = relationship('Genus'          , cascade='all,delete', back_populates='department')
    plant           = relationship('Plant'          , cascade='all,delete', back_populates='department')
    
    


class Class(Base):
    __tablename__   = 'class'
    id              = Column(Integer, primary_key=True, index=True)
    name_lt         = Column(String)
    name_ru         = Column(String)
    name_tm         = Column(String)
    department_id   = Column(Integer, ForeignKey('department.id', ondelete='CASCADE'))
    is_deleted      = Column(Boolean, default=False)
    create_at       = Column(DateTime, default=datetime.now)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    department      = relationship('Department'     , back_populates='class_rel')
    subclass        = relationship('Subclass'       , cascade="all,delete", back_populates='class_rel')
    supersubclass   = relationship('Supersubclass'  , cascade="all,delete", back_populates='class_rel')
    order           = relationship('Order'          , cascade="all,delete", back_populates='class_rel')
    suborder        = relationship('Suborder'       , cascade="all,delete", back_populates='class_rel')
    family          = relationship('Family'         , cascade="all,delete", back_populates='class_rel')
    genus           = relationship('Genus'          , cascade='all,delete', back_populates='class_rel')
    plant           = relationship('Plant'          , cascade='all,delete', back_populates='class_rel')
    
    



class Subclass(Base):
    __tablename__   = 'subclass'
    id              = Column(Integer, primary_key=True, index=True)
    name_lt         = Column(String)
    name_ru         = Column(String)
    name_tm         = Column(String)
    department_id   = Column(Integer, ForeignKey('department.id', ondelete='CASCADE'))
    class_id        = Column(Integer, ForeignKey('class.id', ondelete='CASCADE'))
    is_deleted      = Column(Boolean, default=False)
    create_at       = Column(DateTime, default=datetime.now)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    department      = relationship('Department'     , back_populates='subclass')
    class_rel       = relationship('Class'          , back_populates='subclass')
    supersubclass   = relationship('Supersubclass'  , cascade="all,delete", back_populates='subclass')
    order           = relationship('Order'          , cascade="all,delete", back_populates='subclass')
    suborder        = relationship('Suborder'       , cascade="all,delete", back_populates='subclass')
    family          = relationship('Family'         , cascade="all,delete", back_populates='subclass')
    genus           = relationship('Genus'          , cascade='all,delete', back_populates='subclass')
    plant           = relationship('Plant'          , cascade='all,delete', back_populates='subclass')
    




class Supersubclass(Base):
    __tablename__   = 'supersubclass'
    id              = Column(Integer, primary_key=True, index=True)
    name_lt         = Column(String)
    name_ru         = Column(String)
    name_tm         = Column(String)
    department_id   = Column(Integer, ForeignKey('department.id', ondelete='CASCADE'))
    class_id        = Column(Integer, ForeignKey('class.id', ondelete='CASCADE'))
    subclass_id     = Column(Integer, ForeignKey('subclass.id', ondelete='CASCADE'))
    is_deleted      = Column(Boolean, default=False)
    create_at       = Column(DateTime, default=datetime.now)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    department      = relationship('Department' , back_populates='supersubclass')
    class_rel       = relationship('Class'      , back_populates='supersubclass')
    subclass        = relationship('Subclass'   , back_populates='supersubclass')
    order           = relationship('Order'      , cascade="all,delete", back_populates='supersubclass')
    suborder        = relationship('Suborder'   , cascade="all,delete", back_populates='supersubclass')
    family          = relationship('Family'     , cascade="all,delete", back_populates='supersubclass')
    genus           = relationship('Genus'      , cascade='all,delete', back_populates='supersubclass')
    plant           = relationship('Plant'      , cascade='all,delete', back_populates='supersubclass')
    



class Order(Base):
    __tablename__       = 'order'
    id                  = Column(Integer, primary_key=True, index=True)
    name_lt             = Column(String)
    name_ru             = Column(String)
    name_tm             = Column(String)
    department_id       = Column(Integer, ForeignKey('department.id', ondelete='CASCADE'))
    class_id            = Column(Integer, ForeignKey('class.id', ondelete='CASCADE'))
    subclass_id         = Column(Integer, ForeignKey('subclass.id', ondelete='CASCADE'))
    supersubclass_id    = Column(Integer, ForeignKey('supersubclass.id', ondelete='CASCADE'))
    is_deleted          = Column(Boolean, default=False)
    create_at           = Column(DateTime, default=datetime.now)
    update_at           = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    department      = relationship('Department'     , back_populates='order')
    class_rel       = relationship('Class'          , back_populates='order')
    subclass        = relationship('Subclass'       , back_populates='order')
    supersubclass   = relationship('Supersubclass'  , back_populates='order')
    suborder        = relationship('Suborder'       , cascade="all,delete", back_populates='order')
    family          = relationship('Family'         , cascade="all,delete", back_populates='order')
    genus           = relationship('Genus'          , cascade='all,delete', back_populates='order')
    plant           = relationship('Plant'          , cascade='all,delete', back_populates='order')
    


class Suborder(Base):
    __tablename__       = 'suborder'
    id                  = Column(Integer, primary_key=True, index=True)
    name_lt             = Column(String)
    name_ru             = Column(String)
    name_tm             = Column(String)
    department_id       = Column(Integer, ForeignKey('department.id', ondelete='CASCADE'))
    class_id            = Column(Integer, ForeignKey('class.id', ondelete='CASCADE'))
    subclass_id         = Column(Integer, ForeignKey('subclass.id', ondelete='CASCADE'))
    supersubclass_id    = Column(Integer, ForeignKey('supersubclass.id', ondelete='CASCADE'))
    order_id            = Column(Integer, ForeignKey('order.id', ondelete='CASCADE'))
    is_deleted          = Column(Boolean, default=False)
    create_at           = Column(DateTime, default=datetime.now)
    update_at           = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    department          = relationship('Department'     , back_populates='suborder')
    class_rel           = relationship('Class'          , back_populates='suborder')
    subclass            = relationship('Subclass'       , back_populates='suborder')
    supersubclass       = relationship('Supersubclass'  , back_populates='suborder')
    order               = relationship('Order'          , back_populates='suborder')
    family              = relationship('Family'         , cascade="all,delete", back_populates='suborder')
    genus               = relationship('Genus'          , cascade='all,delete', back_populates='suborder')
    plant               = relationship('Plant'          , cascade='all,delete', back_populates='suborder')
    
    



class Family(Base):
    __tablename__       = 'family'
    id                  = Column(Integer, primary_key=True, index=True)
    name_lt             = Column(String)
    name_ru             = Column(String)
    name_tm             = Column(String)
    family_author       = Column(String)
    department_id       = Column(Integer, ForeignKey('department.id', ondelete='CASCADE'))
    class_id            = Column(Integer, ForeignKey('class.id', ondelete='CASCADE'))
    subclass_id         = Column(Integer, ForeignKey('subclass.id', ondelete='CASCADE'))
    supersubclass_id    = Column(Integer, ForeignKey('supersubclass.id', ondelete='CASCADE'))
    order_id            = Column(Integer, ForeignKey('order.id', ondelete='CASCADE'))
    suborder_id         = Column(Integer, ForeignKey('suborder.id', ondelete='CASCADE'))
    is_deleted          = Column(Boolean, default=False)
    create_at           = Column(DateTime, default=datetime.now)
    update_at           = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    department          = relationship('Department'     , back_populates='family')
    class_rel           = relationship('Class'          , back_populates='family')
    subclass            = relationship('Subclass'       , back_populates='family')
    supersubclass       = relationship('Supersubclass'  , back_populates='family')
    order               = relationship('Order'          , back_populates='family')
    suborder            = relationship('Suborder'       , back_populates='family')
    genus               = relationship('Genus'          , cascade='all,delete', back_populates='family')
    plant               = relationship('Plant'          , cascade='all,delete', back_populates='family')

    family_synonym      = relationship('FamilySynonym'  , cascade='all,delete', back_populates='family')
    
    
    
class FamilySynonym(Base):
    __tablename__       = 'family_synonym'
    id                  = Column(Integer, primary_key=True, index=True)
    name_lt             = Column(String)
    name_ru             = Column(String)
    name_tm             = Column(String)
    family_id           = Column(Integer, ForeignKey('family.id', ondelete='CASCADE'))
    create_at           = Column(DateTime, default=datetime.now)
    update_at           = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    family              = relationship('Family', back_populates='family_synonym')
    
    
class Genus(Base):
    __tablename__       = 'genus'
    id                  = Column(Integer, primary_key=True, index=True)
    name_lt             = Column(String)
    name_ru             = Column(String)
    name_tm             = Column(String)
    genus_author        = Column(String)
    department_id       = Column(Integer, ForeignKey('department.id', ondelete='CASCADE'))
    class_id            = Column(Integer, ForeignKey('class.id', ondelete='CASCADE'))
    subclass_id         = Column(Integer, ForeignKey('subclass.id', ondelete='CASCADE'))
    supersubclass_id    = Column(Integer, ForeignKey('supersubclass.id', ondelete='CASCADE'))
    order_id            = Column(Integer, ForeignKey('order.id', ondelete='CASCADE'))
    suborder_id         = Column(Integer, ForeignKey('suborder.id', ondelete='CASCADE'))
    family_id           = Column(Integer, ForeignKey('family.id', ondelete='CASCADE'))
    is_deleted          = Column(Boolean, default=False)
    create_at           = Column(DateTime, default=datetime.now)
    update_at           = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    department          = relationship('Department'     , back_populates='genus')
    class_rel           = relationship('Class'          , back_populates='genus')
    subclass            = relationship('Subclass'       , back_populates='genus')
    supersubclass       = relationship('Supersubclass'  , back_populates='genus')
    order               = relationship('Order'          , back_populates='genus')
    suborder            = relationship('Suborder'       , back_populates='genus')
    family              = relationship('Family'         , back_populates='genus')
    plant               = relationship('Plant'          , cascade='all,delete', back_populates='genus')
    
    genus_synonym       = relationship('GenusSynonym'   , cascade='all,delete', back_populates='genus')
    
    
    
class GenusSynonym(Base):
    __tablename__       = 'genus_synonym'
    id                  = Column(Integer, primary_key=True, index=True)
    name_lt             = Column(String)
    name_ru             = Column(String)
    name_tm             = Column(String)
    genus_id            = Column(Integer, ForeignKey('genus.id', ondelete='CASCADE'))
    create_at           = Column(DateTime, default=datetime.now)
    update_at           = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    genus               = relationship('Genus'          , back_populates='genus_synonym')
    
    
    
class FullnameSynonym(Base):
    __tablename__       = 'fullname_synonym'
    id                  = Column(Integer, primary_key=True, index=True)
    name                = Column(String)
    plant_id            = Column(Integer, ForeignKey('plant.id', ondelete='CASCADE'))
    create_at           = Column(DateTime, default=datetime.now)
    update_at           = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    plant               = relationship('Plant', back_populates='fullname_synonym')
    
    
class PlantAuthor(Base):
    __tablename__       = 'plant_author'
    id                  = Column(Integer, primary_key=True, index=True)
    name                = Column(String)
    plant_id            = Column(Integer, ForeignKey('plant.id', ondelete='CASCADE'))
    create_at           = Column(DateTime, default=datetime.now)
    update_at           = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    plant               = relationship('Plant', back_populates='plant_author')
    
    
class LinkSynonym(Base):
    __tablename__       = 'link_synonym'
    id                  = Column(Integer, primary_key=True, index=True)
    link                = Column(String)
    plant_id            = Column(Integer, ForeignKey('plant.id', ondelete='CASCADE'))
    create_at           = Column(DateTime, default=datetime.now)
    update_at           = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    plant               = relationship('Plant', back_populates='link_synonym')
    
    
class Plant(Base):
    __tablename__       = 'plant'
    id                  = Column(Integer, primary_key=True, index=True)
    kind                = Column(String)    
    subkind             = Column(String)
    variety             = Column(String)
    form                = Column(String)
    hybrid              = Column(String)
    cultivar            = Column(String)
    name_ru             = Column(String)
    name_kz             = Column(String)
    name_folk           = Column(String)
    fullname            = Column(String)
    fullname_ru         = Column(String)
    department_id       = Column(Integer, ForeignKey('department.id', ondelete='CASCADE'))
    class_id            = Column(Integer, ForeignKey('class.id', ondelete='CASCADE'))
    subclass_id         = Column(Integer, ForeignKey('subclass.id', ondelete='CASCADE'))
    supersubclass_id    = Column(Integer, ForeignKey('supersubclass.id', ondelete='CASCADE'))
    order_id            = Column(Integer, ForeignKey('order.id', ondelete='CASCADE'))
    suborder_id         = Column(Integer, ForeignKey('suborder.id', ondelete='CASCADE'))
    family_id           = Column(Integer, ForeignKey('family.id', ondelete='CASCADE'))
    genus_id            = Column(Integer, ForeignKey('genus.id', ondelete='CASCADE'))
    is_deleted          = Column(Boolean, default=False)
    create_at           = Column(DateTime, default=datetime.now)
    update_at           = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    department          = relationship('Department'     , back_populates='plant')
    class_rel           = relationship('Class'          , back_populates='plant')
    subclass            = relationship('Subclass'       , back_populates='plant')
    supersubclass       = relationship('Supersubclass'  , back_populates='plant')
    order               = relationship('Order'          , back_populates='plant')
    suborder            = relationship('Suborder'       , back_populates='plant')
    family              = relationship('Family'         , back_populates='plant')
    genus               = relationship('Genus'          , back_populates='plant')
    
    fullname_synonym    = relationship('FullnameSynonym', back_populates='plant')
    plant_author        = relationship('PlantAuthor'    , back_populates='plant')
    link_synonym        = relationship('LinkSynonym'    , back_populates='plant')
    
    areal               = relationship('Areals'         , uselist=False, back_populates='plant')
    morphology          = relationship('Morphology'     , uselist=False, back_populates='plant')
    ecology             = relationship('Ecology'        , uselist=False, back_populates='plant')
    note                = relationship('Note'           , uselist=False, back_populates='plant')
    apply               = relationship('Apply'          , uselist=False, back_populates='plant')
    addition            = relationship('Addition'       , uselist=False, back_populates='plant')
    maps                = relationship('Maps'           , uselist=False, back_populates='plant')
    image               = relationship('Image'          , back_populates='plant')
    herbarium           = relationship('Herbarium'      , back_populates='plant')
    
    
    
    
    
    
class Areals(Base):
    __tablename__           = 'areals'
    id                      = Column(Integer, primary_key=True, index=True)
    floristic_regions       = Column(String)
    abbreviated_names       = Column(String)
    old_names               = Column(String)
    study_territory         = Column(String)
    administrative_regions  = Column(String)
    geographic_regions      = Column(String)
    additional_areals       = Column(String)
    general_distribution    = Column(String)
    geo_groups_areals       = Column(String)
    plant_id                = Column(Integer, ForeignKey('plant.id', ondelete='CASCADE'))
    is_deleted              = Column(Boolean, default=False)
    create_at               = Column(DateTime, default=datetime.now)
    update_at               = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    plant                   = relationship('Plant', back_populates='areal')
    
    
class Morphology(Base):
    __tablename__                   = 'morphology'
    id                              = Column(Integer, primary_key=True, index=True)
    growth_form                     = Column(String)
    deciduousness                   = Column(String)
    life_form_raunkier              = Column(String)
    fruit_bearing                   = Column(String)
    type_pollination                = Column(String)
    begin_flowering_decade          = Column(String)
    begin_flowering_month           = Column(String)
    end_flowering_decade            = Column(String)
    end_flowering_month             = Column(String)
    fruit_ripening_decade           = Column(String)
    fruit_ripening_month            = Column(String)
    flower_color_shade              = Column(String)
    flower_color_background         = Column(String)
    fruit_color_shade               = Column(String)
    fruit_color_background          = Column(String)
    leaf_color_summer_shade         = Column(String)
    leaf_color_summer_background    = Column(String)
    leaf_color_autumn_shade         = Column(String)
    leaf_color_autumn_background    = Column(String)
    description_structure           = Column(String)
    additional                      = Column(String)
    plant_id                        = Column(Integer, ForeignKey('plant.id', ondelete='CASCADE'))
    is_deleted                      = Column(Boolean, default=False)
    create_at                       = Column(DateTime, default=datetime.now)
    update_at                       = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    plant                           = relationship('Plant', back_populates='morphology')
    
    
    
class Ecology(Base):
    __tablename__           = 'ecology'
    id                      = Column(Integer, primary_key=True, index=True)
    natural_area            = Column(String)
    vegetation_type         = Column(String)
    vegetation_subtype      = Column(String)
    habitats                = Column(String)
    phytoprotective_status  = Column(String)
    endemicity              = Column(String)
    relic                   = Column(String)
    aboriginality           = Column(String)
    water                   = Column(String)
    soil_fertility          = Column(String)
    soil_salinity           = Column(String)
    light                   = Column(String)
    other_features          = Column(String)
    plant_id                = Column(Integer, ForeignKey('plant.id', ondelete='CASCADE'))
    is_deleted              = Column(Boolean, default=False)
    create_at               = Column(DateTime, default=datetime.now)
    update_at               = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    plant                   = relationship('Plant', back_populates='ecology')
    
    
class Note(Base):
    __tablename__           = 'note'
    id                      = Column(Integer, primary_key=True, index=True)
    text                    = Column(String)
    plant_id                = Column(Integer, ForeignKey('plant.id', ondelete='CASCADE'))
    is_deleted              = Column(Boolean, default=False)
    create_at               = Column(DateTime, default=datetime.now)
    update_at               = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    plant                   = relationship('Plant', back_populates='note')
    
    
    
class Apply(Base):
    __tablename__           = 'apply'
    id                      = Column(Integer, primary_key=True, index=True)
    can_be_used1            = Column(String)
    can_be_used2            = Column(String)
    can_be_used3            = Column(String)
    as_decorative1          = Column(String)
    as_decorative2          = Column(String)
    while_creating          = Column(String)
    for_phytomelioration1   = Column(String)
    for_phytomelioration2   = Column(String)
    for_phytomelioration3   = Column(String)
    as_food                 = Column(String)
    as_feed                 = Column(String)
    as_medicinal            = Column(String)
    as_technical            = Column(String)
    for_other_purposes      = Column(String)
    availability_materials  = Column(String)
    propagated_seeds        = Column(String)
    propagated_vegetatively = Column(String)
    propagated_condition    = Column(String)
    main_ways_prop          = Column(String)
    plant_id                = Column(Integer, ForeignKey('plant.id', ondelete='CASCADE'))
    is_deleted              = Column(Boolean, default=False)
    create_at               = Column(DateTime, default=datetime.now)
    update_at               = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    plant                   = relationship('Plant', back_populates='apply')
    
    
    
class Addition(Base):
    __tablename__       = 'addition'
    id                  = Column(Integer, primary_key=True, index=True)
    red_book1           = Column(String)
    red_book2           = Column(String)
    red_book3           = Column(String)
    source1             = Column(String)
    source2             = Column(String)
    source3             = Column(String)
    source4             = Column(String)
    source5             = Column(String)
    note                = Column(String)
    botanical_institute = Column(String)
    performer_position  = Column(String)
    performer_degree    = Column(String)
    performer_fullname  = Column(String)
    plant_id            = Column(Integer, ForeignKey('plant.id', ondelete='CASCADE'))
    is_deleted          = Column(Boolean, default=False)
    create_at           = Column(DateTime, default=datetime.now)
    update_at           = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    plant               = relationship('Plant', back_populates='addition')
    
    
class Maps(Base):
    __tablename__       = 'maps'
    id                  = Column(Integer, primary_key=True, index=True)
    img_name            = Column(String)
    plant_id            = Column(Integer, ForeignKey('plant.id', ondelete='CASCADE'))
    is_deleted          = Column(Boolean, default=False)
    create_at           = Column(DateTime, default=datetime.now)
    update_at           = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    plant               = relationship('Plant', back_populates='maps')
    
    
    
    
class Image(Base):
    __tablename__       = 'image'
    id                  = Column(Integer, primary_key=True, index=True)
    img_name            = Column(String)
    plant_id            = Column(Integer, ForeignKey('plant.id', ondelete='CASCADE'))
    is_deleted          = Column(Boolean, default=False)
    create_at           = Column(DateTime, default=datetime.now)
    update_at           = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    plant               = relationship('Plant', back_populates='image')
    
    

class Herbarium(Base):
    __tablename__       = 'herbarium'
    id                  = Column(Integer, primary_key=True, index=True)
    img_name            = Column(String, default='')
    date_of_selection   = Column(String)
    region              = Column(String)
    area                = Column(String)
    place_of_selection  = Column(String)
    geo_latitude        = Column(String)
    geo_longitude       = Column(String)
    sea_level           = Column(String)
    plant_id            = Column(Integer, ForeignKey('plant.id', ondelete='CASCADE'))
    is_deleted          = Column(Boolean, default=False)
    create_at           = Column(DateTime, default=datetime.now)
    update_at           = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    plant               = relationship('Plant', back_populates='herbarium')