from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc, func
from tokens import create_access_token, check_token, decode_token
import models



########################
# ADMIN AUTHENTICATION #
########################



# create superadmin
async def create_superadmin(db: Session):
    new_dict = {
        'username'  : 'admin',
        'password'  : 'admin'
    }
    access_token = await create_access_token(data=new_dict)
    new_add = models.Admin(
        username        = 'admin',
        password        = 'admin',
        token           = access_token,
        is_active       = True,
        is_superadmin   = True
    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None



# read all users
async def read_all_users(header_param: Request, db: Session):
    user = await read_user_exist(header_param=header_param, db=db)
    if not user:
        return None
    result = db.query(models.Users)\
        .filter(and_(
            models.Users.is_deleted == False,
        )).order_by(desc(models.Users.id)).distinct().all()
    if result:
        return result
    else:
        return None


# read user
async def read_user(id, header_param: Request, db: Session):
    user = await read_user_exist(header_param=header_param, db=db)
    if not user:
        return None
    result = db.query(models.Users)\
        .filter(and_(
            models.Users.id == id, 
            models.Users.is_deleted == False,
            models.Users.is_active  == True
        )).first()
    if result:
        return result
    else:
        return None


# read all admin
async def read_all_admins(header_param: Request, db: Session):
    user = await read_user_exist(header_param=header_param, db=db)
    if not user:
        return None
    result = db.query(models.Admin)\
        .filter(and_(
            models.Admin.is_deleted == False,
        )).order_by(desc(models.Admin.id)).distinct().all()
    if result:
        return result
    else:
        return None


# read admin
async def read_admin(id, header_param: Request, db: Session):
    user = await read_user_exist(header_param=header_param, db=db)
    if not user:
        return None
    result = db.query(models.Admin)\
        .filter(and_(
            models.Admin.id == id, 
            models.Admin.is_deleted == False,
        )).first()
    if result:
        return result
    else:
        return None


# read admin by username and password
async def read_admin_by_username_password(username: str, password: str, db: Session):
    result = db.query(models.Admin)\
        .filter(and_(
            models.Admin.username   == username, 
            models.Admin.password   == password, 
            models.Admin.is_deleted == False,
            models.Admin.is_active  == True
        )).first()
    if result:
        return result
    else:
        return None


# check existing user
async def read_user_exist(header_param: Request, db: Session):
    token = await check_token(header_param=header_param)
    if not token:
        return None
    payload = await decode_token(token=token)
    if not payload:
        return None
    username: str = payload.get('username')
    password: str = payload.get('password')
    result = await read_admin_by_username_password(username=username, password=password, db=db)
    if result and result.is_superadmin:
        return True
    else:
        return None



# create admin
async def create_admin(req: models.AdminBase, db: Session, header_param):
    user = await read_user_exist(header_param=header_param, db=db)
    if not user:
        return None
    new_dict = {
        'username'  : req.username,
        'password'  : req.password
    }
    access_token = await create_access_token(data=new_dict)
    new_add = models.Admin(
        username        = req.username,
        password        = req.password,
        token           = access_token,
        is_active       = req.is_active,
        is_superadmin   = req.is_superadmin
    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None



# update admin
async def update_admin(id, req: models.AdminBase, header_param: Request, db: Session):
    user = await read_user_exist(header_param=header_param, db=db)
    if not user:
        return None
    new_update = db.query(models.Admin).filter(models.Admin.id == id)\
        .update({
            models.Admin.username   : req.username,
            models.Admin.password   : req.password,
            models.Admin.is_active  : req.is_active,
        }, synchronize_session=False)
    db.commit()
    if new_update:
        return True
    else:
        return None


# set is delete true
async def delete_admin(id, req: models.UserDelete, header_param: Request, db: Session):
    user = await read_user_exist(header_param=header_param, db=db)
    if not user:
        return None
    new_delete = db.query(models.Admin).filter(models.Admin.id == id)\
        .update({
            models.Admin.is_deleted     : req.is_deleted
        }, synchronize_session=False)
    db.commit()
    if new_delete:
        return True
    else:
        return None


# update admin is active
async def update_admin_is_active(id, req: models.UserActiveSet, header_param: Request, db: Session):
    user = await read_user_exist(header_param=header_param, db=db)
    if not user:
        return None
    new_update = db.query(models.Admin).filter(models.Admin.id == id)\
        .update({
            models.Admin.is_active     : req.is_active
        }, synchronize_session=False)
    db.commit()
    if new_update:
        return True
    else:
        return None




#######################
# USER AUTHENTICATION #
#######################


# create user
async def create_user(req: models.UserBase, header_param: Request, db: Session):
    user = await read_user_exist(header_param=header_param, db=db)
    if not user:
        return None
    new_dict = {
        'username'  : req.username,
        'password'  : req.password
    }
    access_token = await create_access_token(data=new_dict)
    new_add = models.Users(
        username    = req.username,
        password    = req.password,
        is_active   = req.is_active,
        token       = access_token
    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None



# update user
async def update_user(id: int, req: models.UserBase, header_param: Request, db: Session):
    user = await read_user_exist(header_param=header_param, db=db)
    if not user:
        return None
    new_update = db.query(models.Users).filter(models.Users.id == id)\
        .update({
            models.Users.username   : req.username,
            models.Users.password   : req.password,
            models.Users.is_active  : req.is_active
        }, synchronize_session=False)
    db.commit()
    if new_update:
        return True
    else:
        return None



# delete user
async def delete_user(id: int, req: models.UserDelete, header_param: Request, db: Session):
    user = await read_user_exist(header_param=header_param, db=db)
    if not user:
        return None
    new_delete = db.query(models.Users).filter(models.Users.id == id)\
        .update({
            models.Users.is_deleted  : req.is_deleted
        }, synchronize_session=False)
    db.commit()
    if new_delete:
        return True
    else:
        return None



# update user is active
async def update_user_is_active(id: int, req: models.UserActiveSet, header_param: Request, db: Session):
    user = await read_user_exist(header_param=header_param, db=db)
    if not user:
        return None
    new_update = db.query(models.Users).filter(models.Users.id == id)\
    .update({
        models.Users.is_active  : req.is_active
    }, synchronize_session=False)
    db.commit()
    if new_update:
        return True
    else:
        return None