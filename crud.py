from fastapi import Request
from sqlalchemy.orm import Session, joinedload
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, or_, desc, asc, func
from tokens import create_access_token, check_token, decode_token
import models as mod



########################
# ADMIN AUTHENTICATION #
########################


async def admin_login(req: mod.LoginSchema, db: Session):
    result = await read_admin_by_username_password(req.username, req.password, db)
    if result:
        return result
    else:
        return None


# read admin by username and password
async def read_admin_by_username_password(username: str, password: str, db: Session):
    result = db.query(mod.Admin)\
        .filter(and_(
            mod.Admin.username   == username, 
            mod.Admin.password   == password, 
            mod.Admin.is_deleted == False,
            mod.Admin.is_active  == True
        )).first()
    if result:
        return result
    else:
        return None



# check admin is superadmin
async def check_admin_is_superadmin(header_param: Request, db: Session):
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



# create superadmin
async def create_superadmin(db: Session):
    new_dict = {
        'username'  : 'admin',
        'password'  : 'admin'
    }
    access_token = await create_access_token(data=new_dict)
    new_add = mod.Admin(
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
    user = await check_admin_is_superadmin(header_param=header_param, db=db)
    if not user:
        return None
    result = db.query(mod.Users)\
        .filter(and_(
            mod.Users.is_deleted == False,
        )).order_by(desc(mod.Users.id)).distinct().all()
    if result:
        return result
    else:
        return None


# read user
async def read_user(id, header_param: Request, db: Session):
    user = await check_admin_is_superadmin(header_param=header_param, db=db)
    if not user:
        return None
    result = db.query(mod.Users)\
        .filter(and_(
            mod.Users.id == id, 
            mod.Users.is_deleted == False,
        )).first()
    if result:
        return result
    else:
        return None


# read all admin
async def read_all_admins(header_param: Request, db: Session):
    user = await check_admin_is_superadmin(header_param=header_param, db=db)
    if not user:
        return None
    result = db.query(mod.Admin)\
        .filter(and_(
            mod.Admin.is_deleted == False,
        )).order_by(desc(mod.Admin.id)).distinct().all()
    if result:
        return result
    else:
        return None


# read admin
async def read_admin(id, header_param: Request, db: Session):
    user = await check_admin_is_superadmin(header_param=header_param, db=db)
    if not user:
        return None
    result = db.query(mod.Admin)\
        .filter(and_(
            mod.Admin.id == id, 
            mod.Admin.is_deleted == False,
        )).first()
    if result:
        return result
    else:
        return None



# create admin
async def create_admin(req: mod.AdminBase, db: Session, header_param):
    user = await check_admin_is_superadmin(header_param=header_param, db=db)
    if not user:
        return None
    new_dict = {
        'username'  : req.username,
        'password'  : req.password
    }
    access_token = await create_access_token(data=new_dict)
    new_add = mod.Admin(
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
async def update_admin(id, req: mod.AdminBase, header_param: Request, db: Session):
    user = await check_admin_is_superadmin(header_param=header_param, db=db)
    if not user:
        return None
    new_update = db.query(mod.Admin).filter(mod.Admin.id == id)\
        .update({
            mod.Admin.username   : req.username,
            mod.Admin.password   : req.password,
            mod.Admin.is_active  : req.is_active,
        }, synchronize_session=False)
    db.commit()
    if new_update:
        return True
    else:
        return None


# set is delete true
async def delete_admin(id, req: mod.UserDelete, header_param: Request, db: Session):
    user = await check_admin_is_superadmin(header_param=header_param, db=db)
    if not user:
        return None
    new_delete = db.query(mod.Admin).filter(mod.Admin.id == id)\
        .update({
            mod.Admin.is_deleted     : req.is_deleted
        }, synchronize_session=False)
    db.commit()
    if new_delete:
        return True
    else:
        return None


# update admin is active
async def update_admin_is_active(id, req: mod.UserActiveSet, header_param: Request, db: Session):
    user = await check_admin_is_superadmin(header_param=header_param, db=db)
    if not user:
        return None
    new_update = db.query(mod.Admin).filter(mod.Admin.id == id)\
        .update({
            mod.Admin.is_active     : req.is_active
        }, synchronize_session=False)
    db.commit()
    if new_update:
        return True
    else:
        return None




#######################
# USER AUTHENTICATION #
#######################


# read user by username and password
async def read_user_by_username_password(username: str, password: str, db: Session):
    result = db.query(mod.Users)\
        .filter(and_(
            mod.Users.username == username,
            mod.Users.password == password,
            mod.Users.is_deleted == False,
            mod.Users.is_active == True
        )).first()
    if result:
        return True
    else:
        return False



# user login
async def user_login(req: mod.LoginSchema, db: Session):
    result = await read_user_by_username_password(req.username, req.password, db)
    if result:
        return result
    else:
        return None



# create user
async def create_user(req: mod.UserBase, header_param: Request, db: Session):
    user = await check_admin_is_superadmin(header_param=header_param, db=db)
    if not user:
        return None
    new_dict = {
        'username'  : req.username,
        'password'  : req.password
    }
    access_token = await create_access_token(data=new_dict)
    new_add = mod.Users(
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
async def update_user(id: int, req: mod.UserBase, header_param: Request, db: Session):
    user = await check_admin_is_superadmin(header_param=header_param, db=db)
    if not user:
        return None
    new_update = db.query(mod.Users).filter(mod.Users.id == id)\
        .update({
            mod.Users.username   : req.username,
            mod.Users.password   : req.password,
            mod.Users.is_active  : req.is_active
        }, synchronize_session=False)
    db.commit()
    if new_update:
        return True
    else:
        return None



# delete user
async def delete_user(id: int, req: mod.UserDelete, header_param: Request, db: Session):
    user = await check_admin_is_superadmin(header_param=header_param, db=db)
    if not user:
        return None
    new_delete = db.query(mod.Users).filter(mod.Users.id == id)\
        .update({
            mod.Users.is_deleted  : req.is_deleted
        }, synchronize_session=False)
    db.commit()
    if new_delete:
        return True
    else:
        return None



# update user is active
async def update_user_is_active(id: int, req: mod.UserActiveSet, header_param: Request, db: Session):
    user = await check_admin_is_superadmin(header_param=header_param, db=db)
    if not user:
        return None
    new_update = db.query(mod.Users).filter(mod.Users.id == id)\
    .update({
        mod.Users.is_active  : req.is_active
    }, synchronize_session=False)
    db.commit()
    if new_update:
        return True
    else:
        return None




async def check_admin_token(header_param: Request, db: Session):
    token = await check_token(header_param=header_param)
    if not token:
        return None
    payload = await decode_token(token=token)
    if not payload:
        return None
    username: str = payload.get('username')
    password: str = payload.get('password')
    result = await read_admin_by_username_password(username=username, password=password, db=db)
    if result:
        return True
    else:
        return None


async def check_user_token(header_param: Request, db: Session):
    token = await check_token(header_param=header_param)
    if not token:
        return None
    payload = await decode_token(token=token)
    if not payload:
        return None
    username: str = payload.get('username')
    password: str = payload.get('password')
    result = await read_user_by_username_password(username=username, password=password, db=db)
    if result:
        return True
    else:
        return None



##############
# DEPARTMENT #
##############



async def create_department(header_param: Request, req: mod.DepartmentSchema, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return None
    new_add = mod.Department(**req.dict())
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None




async def update_department(id, header_param, req: mod.DepartmentSchema, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return None
    req_json = jsonable_encoder(req)
    new_update = db.query(mod.Department).filter(mod.Department.id == id)\
        .update(req_json, synchronize_session=False)
    db.commit()
    if new_update:
        return True
    else:
        return None




async def read_admin_departments(header_param, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return None
    result = db.query(mod.Department)\
        .options(joinedload(mod.Department.class_rel)\
            .options(joinedload(mod.Class.subclass)\
                .options(joinedload(mod.Subclass.supersubclass)))
        ).filter(mod.Department.is_deleted == False).order_by(desc(mod.Department.id)).all()
    if result:
        return result
    else:
        return None




#########
# CLASS #
#########


async def create_class(req: mod.ClassSchema, header_param, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return None
    new_add = mod.Class(
        name_lt     = req.name_lt,
        name_ru     = req.name_ru,
        department_id   = req.department_id
    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None



async def update_class(id, header_param, req: mod.ClassSchema, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return None
    req_json = jsonable_encoder(req)
    new_update = db.query(mod.Class).filter(mod.Class.id == id)\
        .update(req_json, synchronize_session=False)
    db.commit()
    if new_update:
        return True
    else:
        return None    



async def read_admin_classes(header_param: Request, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return None
    result = db.query(mod.Class)\
        .options(joinedload(mod.Class.subclass)\
            .options(joinedload(mod.Subclass.supersubclass))
        ).filter(mod.Class.is_deleted == False).order_by(desc(mod.Class.id)).all()
    if result:
        return result
    else:
        return None





############
# SUBCLASS #
############



async def create_subclass(header_param, req: mod.SubclassSchema, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return None
    new_add = mod.Subclass(**req.dict())
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None



async def update_subclass(id, header_param, req: mod.SubclassSchema, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return None
    req_json = jsonable_encoder(req)
    new_update = db.query(mod.Subclass).filter(mod.Subclass.id == id)\
        .update(req_json, synchronize_session=False)
    db.commit()
    if new_update:
        return True
    else:
        return None



async def read_admin_subclass(header_param, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return None
    result = db.query(mod.Subclass)\
        .options(joinedload(mod.Subclass.supersubclass))\
            .filter(mod.Subclass.is_deleted == False).order_by(desc(mod.Subclass.id)).all()
    if result:
        return result
    else:
        return None





#################
# SUPERSUBCLASS #
#################



async def create_supersubclass(header_param: Request, req: mod.SupersubclassSchema, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return None
    new_add = mod.Supersubclass(**req.dict())
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None



async def update_supersubclass(id, header_param: Request, req: mod.SupersubclassSchema, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return None
    req_json = jsonable_encoder(req)
    new_update = db.query(mod.Supersubclass).filter(mod.Supersubclass.id == id)\
        .update(req_json, synchronize_session=False)
    db.commit()
    if new_update:
        return True
    else:
        return None



async def read_admin_supersubclass(header_param: Request, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return None
    result = db.query(mod.Supersubclass)\
        .filter(mod.Supersubclass.is_deleted == False).order_by(desc(mod.Supersubclass.id)).all()
    if result:
        return result
    else:
        return None