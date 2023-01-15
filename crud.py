from fastapi import Request, Response
from sqlalchemy.orm import Session, joinedload
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, or_, desc, asc, func
from returns import Returns
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
    result = db.query(
        mod.Admin.id,
        mod.Admin.username,
        mod.Admin.token,
        mod.Admin.is_superadmin
    )\
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
async def create_superadmin(req: mod.AdminBase, db: Session):
    new_delete = db.query(mod.Admin).filter(mod.Admin.is_superadmin == True)\
        .delete(synchronize_session=False)
    db.commit()
    new_dict = {
        'username'  : req.username,
        'password'  : req.password
    }
    access_token = await create_access_token(data=new_dict)
    new_add = mod.Admin(
        username        = req.username,
        password        = req.password,
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
        return -1
    result = db.query(
        mod.Users.id,
        mod.Users.username,
        mod.Users.password,
        mod.Users.is_active,
        mod.Users.create_at,
        mod.Users.update_at
    )\
        .filter(and_(
            mod.Users.is_deleted == False,
        )).order_by(desc(mod.Users.id)).distinct().all()
    return result


# read user
async def read_user(id, header_param: Request, db: Session):
    user = await check_admin_is_superadmin(header_param=header_param, db=db)
    if not user:
        return -1
    result = db.query(mod.Users)\
        .filter(and_(
            mod.Users.id == id, 
            mod.Users.is_deleted == False,
        )).first()
    return result

# read all admin
async def read_all_admins(header_param: Request, db: Session):
    user = await check_admin_is_superadmin(header_param=header_param, db=db)
    if not user:
        return -1
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
        return -1
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
        return -1
    if req.username == "" or req.password == "" or ' ' in req.username or ' ' in req.password:
        return None
    user_exist = db.query(mod.Admin)\
        .filter(mod.Users.username == req.username).first()
    if user_exist:
        return -2
    new_dict = {
        'username'  : req.username,
        'password'  : req.password
    }
    access_token = await create_access_token(data=new_dict)
    new_add = mod.Admin(
        username        = req.username,
        password        = req.password,
        token           = access_token,
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
        return -1
    user_exist = db.query(mod.Admin)\
        .filter(and_(mod.Admin.username == req.username)).first()
    
    if user_exist and user_exist.id != id:
        return -2
    req_json = jsonable_encoder(req)
    new_update = db.query(mod.Admin).filter(mod.Admin.id == id)\
        .update(req_json, synchronize_session=False)
    db.commit()
    if new_update:
        return True
    else:
        return None


# set is delete true
async def delete_admin(id, req: mod.UserDelete, header_param: Request, db: Session):
    user = await check_admin_is_superadmin(header_param=header_param, db=db)
    if not user:
        return -1
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
        return -1
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
    result = db.query(
        mod.Users.id,
        mod.Users.username,
        mod.Users.token
    )\
        .filter(and_(
            mod.Users.username == username,
            mod.Users.password == password,
            mod.Users.is_deleted == False,
            mod.Users.is_active == True
        )).first()
    if result:
        return result
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
        return -1
    if req.username == "" or req.password == "" or ' ' in req.username or ' ' in req.password:
        return None
    user_exist = db.query(mod.Users)\
        .filter(mod.Users.username == req.username).first()
    if user_exist:
        return -2
    new_dict = {
        'username'  : req.username,
        'password'  : req.password
    }
    access_token = await create_access_token(data=new_dict)
    new_add = mod.Users(
        username    = req.username,
        password    = req.password,
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
        return -1
    user_exist = db.query(mod.Users)\
        .filter(and_(mod.Users.username == req.username)).first()
    
    if user_exist and user_exist.id != id:
        return -2
    req_json = jsonable_encoder(req)
    new_update = db.query(mod.Users).filter(mod.Users.id == id)\
        .update(req_json, synchronize_session=False)
    db.commit()
    if new_update:
        return True
    else:
        return None



# delete user
async def delete_user(id: int, req: mod.UserDelete, header_param: Request, db: Session):
    user = await check_admin_is_superadmin(header_param=header_param, db=db)
    if not user:
        return -1
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
        return -1
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
        return -1
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
        return -1
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
        return -1
    result = db.query(mod.Department)\
        .options(joinedload(mod.Department.class_rel)\
            .options(joinedload(mod.Class.subclass)\
                .options(joinedload(mod.Subclass.supersubclass)\
                    .options(joinedload(mod.Supersubclass.order)\
                        .options(joinedload(mod.Order.suborder)\
                            .options(joinedload(mod.Suborder.family)\
                                .options(joinedload(mod.Family.genus))))))))\
                                    .filter(mod.Department.is_deleted == False)\
                                        .order_by(desc(mod.Department.id)).all()
    if result:
        return result
    else:
        return None




async def delete_department(id, header_param: Request, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return -1
    new_delete = db.query(mod.Department).filter(mod.Department.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    if new_delete:
        result = {'msg': 'Удалено!'}
        return result
    

#########
# CLASS #
#########


async def create_class(req: mod.ClassSchema, header_param, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return -1
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
        return -1
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
        return -1
    result = db.query(mod.Class)\
        .options(joinedload(mod.Class.subclass)\
            .options(joinedload(mod.Subclass.supersubclass)\
                .options(joinedload(mod.Supersubclass.order)\
                    .options(joinedload(mod.Order.suborder)\
                        .options(joinedload(mod.Suborder.family))))))\
                            .filter(mod.Class.is_deleted == False)\
                                .order_by(desc(mod.Class.id)).all()
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
        return -1
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
        return -1
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
        return -1
    result = db.query(mod.Subclass)\
        .options(joinedload(mod.Subclass.supersubclass)\
            .options(joinedload(mod.Supersubclass.order)\
                .options(joinedload(mod.Order.suborder)\
                    .options(joinedload(mod.Suborder.family)))))\
                        .filter(mod.Subclass.is_deleted == False)\
                            .order_by(desc(mod.Subclass.id)).all()
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
        return -1
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
        return -1
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
        return -1
    result = db.query(mod.Supersubclass)\
        .options(joinedload(mod.Supersubclass.order)\
            .options(joinedload(mod.Order.suborder)\
                .options(joinedload(mod.Suborder.family))))\
                    .filter(mod.Supersubclass.is_deleted == False)\
                        .order_by(desc(mod.Supersubclass.id)).all()
    if result:
        return result
    else:
        return None



#########
# ORDER #
#########


async def create_order(header_param: Request, req: mod.OrderSchema, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return -1
    new_add = mod.Order(**req.dict())
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None



async def update_order(id: int, header_param: Request, req: mod.OrderSchema, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return -1
    req_json = jsonable_encoder(req)
    new_update = db.query(mod.Order).filter(mod.Order.id == id)\
        .update(req_json, synchronize_session=False)
    db.commit()
    if new_update:
        return True
    else:
        return None



async def read_admin_order(header_param: Request, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return -1
    result = db.query(mod.Order)\
        .options(joinedload(mod.Order.suborder)\
            .options(joinedload(mod.Suborder.family)))\
                .filter(mod.Order.is_deleted == False)\
                    .order_by(desc(mod.Order.id)).all()
    if result:
        return result
    else:
        return None




############
# SUBORDER #
############


async def create_suborder(header_param, req, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return -1
    new_add = mod.Suborder(**req.dict())
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None
    
    

async def update_suborder(id, header_param, req, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return -1
    req_json = jsonable_encoder(req)
    new_update = db.query(mod.Suborder).filter(mod.Suborder.id == id)\
        .update(req_json, synchronize_session=False)
    db.commit()
    if new_update:
        return True
    else:
        return None
    
    
async def read_admin_suborder(header_param, db: Session):
    user = await check_admin_token(header_param=header_param, db=db)
    if not user:
        return -1
    result = db.query(mod.Suborder)\
        .options(joinedload(mod.Suborder.family))\
            .filter(mod.Suborder.is_deleted == False)\
                .order_by(desc(mod.Suborder.id)).all()
    if result:
        return result
    else:
        return None
    
    
    
##########
# FAMILY #
##########


async def create_family(header_param: Request, req: mod.FamilySchema, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_add = mod.Family(**req.dict())
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    
    
    
async def update_family(id, header_param: Request, req: mod.FamilySchema, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    req_json = jsonable_encoder(req)
    new_update = db.query(mod.Family).filter(mod.Family.id == id)\
        .update(req_json, synchronize_session=False)
    db.commit()
    if new_update:
        return True 
    
    
    
async def read_admin_family(header_param: Request, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    result = db.query(mod.Family)\
        .options(joinedload(mod.Family.family_synonym))\
            .filter(mod.Family.is_deleted == False)\
                .order_by(desc(mod.Family.id)).all()
    if result:
        return result
    
    
    
async def delete_family(id, header_param: Request, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_delete = db.query(mod.Family).filter(mod.Family.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    if new_delete:
        result = {'msg': 'Удалено!'}
        return result

    
async def create_family_synonym(header_param: Request, req: mod.FamilySynonymSchema, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_add = mod.FamilySynonym(**req.dict())
    if new_add:
       db.add(new_add)
       db.commit()
       db.refresh(new_add)
       return new_add


async def delete_family_synonym(id: int, header_param: Request, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_delete = db.query(mod.FamilySynonym).filter(mod.FamilySynonym.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    if new_delete:
        result = {'msg': 'Удалено!'}
        return result
    
    
    
#########
# GENUS #
#########


async def create_genus(header_param: Request, req: mod.GenusSchema, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_add = mod.Genus(**req.dict())
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    
    
async def update_genus(id: int, header_param: Request, req: mod.GenusSchema, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    req_json = jsonable_encoder(req)
    new_update = db.query(mod.Genus).filter(mod.Genus.id == id)\
        .update(req_json, synchronize_session=False)
    db.commit()
    if new_update:
        result = {'msg': 'Обновлено!'}
        return result
    
    
async def read_admin_genus(header_param: Request, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    result = db.query(mod.Genus)\
        .options(joinedload(mod.Genus.genus_synonym))\
            .filter(mod.Genus.is_deleted == False).all()
    if result:
        return result
    
    
async def delete_genus(id: int, header_param: Request, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_delete = db.query(mod.Genus).filter(mod.Genus.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    if new_delete:
        result = {'msg': 'Удалено!'}
        return result
    
    
    
    
async def create_genus_synonym(header_param: Request, req: mod.GenusSynonymSchema, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_add = mod.GenusSynonym(**req.dict())
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    
    
async def delete_genus_synonym(id: int, header_param: Request, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_delete = db.query(mod.GenusSynonym).filter(mod.GenusSynonym.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    if new_delete:
        result = {'msg': 'Удалено!'}
        return result
    
    
    
#########
# PLANT #
#########


async def create_plant(header_param: Request, req: mod.PlantSchema, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_add = mod.Plant(
        kind                = req.kind,
        subkind             = req.subkind,
        variety             = req.variety,
        form                = req.form,
        hybrid              = req.hybrid,
        cultivar            = req.cultivar,
        name_ru             = req.name_ru,
        name_kz             = req.name_kz,
        name_folk           = req.name_folk,
        fullname            = req.fullname,
        fullname_ru         = req.fullname_ru,
        department_id       = req.department_id,
        class_id            = req.class_id,
        subclass_id         = req.subclass_id,
        supersubclass_id    = req.supersubclass_id,
        order_id            = req.order_id,
        suborder_id         = req.suborder_id,
        family_id           = req.family_id,
        genus_id            = req.genus_id
    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        
    objects = []

    for obj in req.fullname_synonym:
        obj = jsonable_encoder(obj)
        obj['plant_id'] = new_add.id
        db_item = mod.FullnameSynonym(name = obj['name'], plant_id = obj['plant_id'])
        objects.append(db_item)
    

    for obj in req.plant_author:
        obj = jsonable_encoder(obj)
        obj['plant_id'] = new_add.id
        db_item = mod.PlantAuthor(name = obj['name'], plant_id = obj['plant_id'])
        objects.append(db_item)
    

    for obj in req.link_synonym:
        obj = jsonable_encoder(obj)
        obj['plant_id'] = new_add.id
        db_item = mod.LinkSynonym(link = obj['link'], plant_id = obj['plant_id'])
        objects.append(db_item)

    db.bulk_save_objects(objects)
    db.commit()
    
    if objects:
        return {'msg': 'Создано!'}  
    
    
async def update_plant(id, header_param: Request, req: mod.PlantSchemaUpdate, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    req_json = jsonable_encoder(req)
    new_update = db.query(mod.Plant).filter(mod.Plant.id == id)\
        .update(req_json, synchronize_session=False)
    db.commit()
    if new_update:
        result = {'msg': 'Обновлено!'}
        return result
    
    
async def read_admin_plant(header_param: Request, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    result = db.query(mod.Plant)\
        .options(joinedload(mod.Plant.fullname_synonym))\
            .options(joinedload(mod.Plant.plant_author))\
                .options(joinedload(mod.Plant.link_synonym))\
                    .options(joinedload(mod.Plant.areal))\
                        .options(joinedload(mod.Plant.morphology))\
                            .options(joinedload(mod.Plant.ecology))\
                                .options(joinedload(mod.Plant.note))\
                                    .filter(mod.Plant.is_deleted == False)\
                                        .order_by(desc(mod.Plant.id)).all()
    if result:
        return result
    
    
async def delete_plant(id, header_param: Request, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_delete = db.query(mod.Plant).filter(mod.Plant.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    if new_delete:
        result = {'msg': 'Удалено!'}
        return result
    
    
####################
# PLANT ADDITIONAL #
####################


async def create_fullname_synonym(header_param: Request, req: mod.FullnameSynonymCreateSchema, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_add = mod.FullnameSynonym(**req.dict())
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    
    
    
    
async def delete_fullname_synonym(id, header_param: Request, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_delete = db.query(mod.FullnameSynonym).filter(mod.FullnameSynonym.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    if new_delete:
        return Returns.delete
    
    
    
async def create_link_synonym(header_param: Request, req: mod.LinkSynonymCreateSchema, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_add = mod.LinkSynonym(**req.dict())
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    
    
async def delete_link_synonym(id, header_param: Request, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_delete = db.query(mod.LinkSynonym).filter(mod.LinkSynonym.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    if new_delete:
        return Returns.delete
    
    
async def create_plant_author(header_param: Request, req: mod.PlantAuthorCreateSchema, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_add = mod.PlantAuthor(**req.dict())
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    
    
async def delete_plant_author(id, header_param: Request, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_delete = db.query(mod.PlantAuthor).filter(mod.PlantAuthor.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    if new_delete:
        return Returns.delete
    
    
##########
# AREALS #
##########


async def create_areals(header_param: Request, req: mod.ArealSchema, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_add = mod.Areals(**req.dict())
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    
    
async def read_areal(id, header_param: Request, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    result = db.query(mod.Areals).filter(and_(
        mod.Areals.plant_id == id,
        mod.Areals.is_deleted == False
    )).order_by(desc(mod.Areals.id)).all()
    if result:
        return result
    
    
    
async def update_areal(id: int, header_param: Request, req: mod.ArealSchema, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    req_json = jsonable_encoder(req)
    new_update = db.query(mod.Areals).filter(mod.Areals.id == id)\
        .update(req_json, synchronize_session=False)
    db.commit()
    if new_update:
        return Returns.update
    
    
async def delete_areal(id: int, header_param: Request, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1 
    new_delete = db.query(mod.Areals).filter(mod.Areals.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    if new_delete:
        return Returns.delete
        
        

##############
# MORPHOLOGY #
##############


async def create_morphology(header_param: Request, req: mod.MorphologySchema, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1 
    new_add = mod.Morphology(**req.dict())
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    
    
async def read_morphology(id, header_param: Request, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1 
    result = db.query(mod.Morphology).filter(and_(
        mod.Morphology.plant_id == id,
        mod.Morphology.is_deleted == False
    )).order_by(desc(mod.Morphology.id)).all()
    if result:
        return result
    
    
async def update_morphology(id: int, header_param: Request, req: mod.MorphologySchema, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1 
    req_json = jsonable_encoder(req)
    new_update = db.query(mod.Morphology).filter(mod.Morphology.id == id)\
        .update(req_json, synchronize_session=False)
    db.commit()
    if new_update:
        return Returns.update
    
    
    
async def delete_morphology(id: int, header_param: Request, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_delete = db.query(mod.Morphology).filter(mod.Morphology.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    if new_delete:
        return Returns.delete
    
    
    
###########
# ECOLOGY #
###########


async def create_ecology(header_param: Request, req: mod.EcologySchema, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_add = mod.Ecology(**req.dict())
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    
    
async def update_ecology(id: int, header_param: Request, req: mod.EcologySchema, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    req_json = jsonable_encoder(req)
    new_update = db.query(mod.Ecology).filter(mod.Ecology.id == id)\
        .update(req_json, synchronize_session=False)
    db.commit()
    if new_update:
        return Returns.update
    
    
    
async def delete_ecology(id: int, header_param: Request, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_delete = db.query(mod.Ecology).filter(mod.Ecology.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    if new_delete:
        return Returns.delete
    
    
    
#########
# NOTES #
#########


async def create_note(header_param: Request, req: mod.NoteSchema, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_add = mod.Note(**req.dict())
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    
    
    
async def update_note(id: int, header_param: Request, req: mod.NoteSchema, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    req_json = jsonable_encoder(req)
    new_update = db.query(mod.Note).filter(mod.Note.id == id)\
        .update(req_json, synchronize_session=False)
    db.commit()
    if new_update:
        return Returns.update
    
    
    
async def delete_note(id, header_param: Request, db: Session):
    user = await check_admin_token(header_param, db)
    if not user:
        return -1
    new_delete = db.query(mod.Note).filter(mod.Note.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    if new_delete:
        return Returns.delete