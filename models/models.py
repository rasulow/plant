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
    is_active       = Column(Boolean, default=False)
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


# plant
class Department(Base):
    __tablename__   = 'department'
    id              = Column(Integer, primary_key=True, index=True)
    name_lt         = Column(String)
    name_ru         = Column(String)
    is_deleted      = Column(Boolean, default=False)
    create_at       = Column(DateTime, default=datetime.now)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    class_rel       = relationship('Class'          , back_populates='department')
    subclass        = relationship('Subclass'       , back_populates='department')
    supersubclass   = relationship('Supersubclass'  , back_populates='department')


class Class(Base):
    __tablename__   = 'class'
    id              = Column(Integer, primary_key=True, index=True)
    name_lt         = Column(String)
    name_ru         = Column(String)
    department_id   = Column(Integer, ForeignKey('department.id'))
    is_deleted      = Column(Boolean, default=False)
    create_at       = Column(DateTime, default=datetime.now)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    department      = relationship('Department'     , back_populates='class_rel')
    subclass        = relationship('Subclass'       , back_populates='class_rel')
    supersubclass   = relationship('Supersubclass'  , back_populates='class_rel')



class Subclass(Base):
    __tablename__   = 'subclass'
    id              = Column(Integer, primary_key=True, index=True)
    name_lt         = Column(String)
    name_ru         = Column(String)
    department_id   = Column(Integer, ForeignKey('department.id'))
    class_id        = Column(Integer, ForeignKey('class.id'))
    is_deleted      = Column(Boolean, default=False)
    create_at       = Column(DateTime, default=datetime.now)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    department      = relationship('Department'     , back_populates='subclass')
    class_rel       = relationship('Class'          , back_populates='subclass')
    supersubclass   = relationship('Supersubclass'  , back_populates='subclass')



class Supersubclass(Base):
    __tablename__   = 'supersubclass'
    id              = Column(Integer, primary_key=True, index=True)
    name_lt         = Column(String)
    name_ru         = Column(String)
    department_id   = Column(Integer, ForeignKey('department.id'))
    class_id        = Column(Integer, ForeignKey('class.id'))
    subclass_id     = Column(Integer, ForeignKey('subclass.id'))
    is_deleted      = Column(Boolean, default=False)
    create_at       = Column(DateTime, default=datetime.now)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    department      = relationship('Department' , back_populates='supersubclass')
    class_rel       = relationship('Class'      , back_populates='supersubclass')
    subclass        = relationship('Subclass'   , back_populates='supersubclass')
