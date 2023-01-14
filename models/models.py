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
    family_id           = Column(Integer, ForeignKey('family.id', ondelete='CASCADE'))
    create_at           = Column(DateTime, default=datetime.now)
    update_at           = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    family              = relationship('Family', back_populates='family_synonym')
    
    
class Genus(Base):
    __tablename__       = 'genus'
    id                  = Column(Integer, primary_key=True, index=True)
    name_lt             = Column(String)
    name_ru             = Column(String)
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