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

    class_rel       = relationship('Class', back_populates='department')


class Class(Base):
    __tablename__   = 'class'
    id              = Column(Integer, primary_key=True, index=True)
    name_lt         = Column(String)
    name_ru         = Column(String)
    deaprtment_id   = Column(Integer, ForeignKey('department.id'))
    is_deleted      = Column(Boolean, default=False)
    create_at       = Column(DateTime, default=datetime.now)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    department      = relationship('Department', back_populates='class_rel')