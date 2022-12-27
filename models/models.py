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

    class_rel       = relationship('Class'          , cascade="all, delete", back_populates='department')
    subclass        = relationship('Subclass'       , cascade="all, delete", back_populates='department')
    supersubclass   = relationship('Supersubclass'  , cascade="all, delete", back_populates='department')
    order           = relationship('Order'          , cascade="all, delete", back_populates='department')
    suborder        = relationship('Suborder'       , cascade="all, delete", back_populates='department')


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
    subclass        = relationship('Subclass'       , cascade="all, delete", back_populates='class_rel')
    supersubclass   = relationship('Supersubclass'  , cascade="all, delete", back_populates='class_rel')
    order           = relationship('Order'          , cascade="all, delete", back_populates='class_rel')
    suborder        = relationship('Suborder'       , cascade="all, delete", back_populates='class_rel')



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
    supersubclass   = relationship('Supersubclass'  , cascade="all, delete", back_populates='subclass')
    order           = relationship('Order'          , cascade="all, delete", back_populates='subclass')
    suborder        = relationship('Suborder'       , cascade="all, delete", back_populates='subclass')




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
    order           = relationship('Order'      , cascade="all, delete", back_populates='supersubclass')
    suborder        = relationship('Suborder'   , cascade="all, delete", back_populates='supersubclass')



class Order(Base):
    __tablename__       = 'order'
    id                  = Column(Integer, primary_key=True, index=True)
    name_lt             = Column(String)
    name_ru             = Column(String)
    department_id       = Column(Integer, ForeignKey('department.id'))
    class_id            = Column(Integer, ForeignKey('class.id'))
    subclass_id         = Column(Integer, ForeignKey('subclass.id'))
    supersubclass_id    = Column(Integer, ForeignKey('supersubclass.id'))
    is_deleted          = Column(Boolean, default=False)
    create_at           = Column(DateTime, default=datetime.now)
    update_at           = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    department      = relationship('Department'     , back_populates='order')
    class_rel       = relationship('Class'          , back_populates='order')
    subclass        = relationship('Subclass'       , back_populates='order')
    supersubclass   = relationship('Supersubclass'  , back_populates='order')
    suborder        = relationship('Suborder'       , cascade="all, delete", back_populates='order')


class Suborder(Base):
    __tablename__       = 'suborder'
    id                  = Column(Integer, primary_key=True, index=True)
    name_lt             = Column(String)
    name_ru             = Column(String)
    department_id       = Column(Integer, ForeignKey('department.id'))
    class_id            = Column(Integer, ForeignKey('class.id'))
    subclass_id         = Column(Integer, ForeignKey('subclass.id'))
    supersubclass_id    = Column(Integer, ForeignKey('supersubclass.id'))
    order_id            = Column(Integer, ForeignKey('order.id'))
    is_deleted          = Column(Boolean, default=False)
    create_at           = Column(DateTime, default=datetime.now)
    update_at           = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    department          = relationship('Department'     , back_populates='suborder')
    class_rel           = relationship('Class'          , back_populates='suborder')
    subclass            = relationship('Subclass'       , back_populates='suborder')
    supersubclass       = relationship('Supersubclass'  , back_populates='suborder')
    order               = relationship('Order'          , back_populates='suborder')
