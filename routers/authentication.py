from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
import crud
import models
from returns import Returns


authentication_router = APIRouter()


@authentication_router.get('/api/get-users', dependencies=[Depends(HTTPBearer())])
async def get_users(header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_all_users(header_param = header_param, db=db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL


@authentication_router.get('/api/get-user/{id}', dependencies=[Depends(HTTPBearer())])
async def get_user(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_user(id=id, header_param=header_param, db=db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL


@authentication_router.get('/api/get-admins', dependencies=[Depends(HTTPBearer())])
async def get_admins(header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_all_admins(header_param=header_param, db=db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL


@authentication_router.get('/api/get-admin/{id}', dependencies=[Depends(HTTPBearer())])
async def get_admin(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_admin(id=id, header_param=header_param, db=db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL


@authentication_router.post('/api/create-admin', dependencies=[Depends(HTTPBearer())])
async def create_admin(header_param: Request, req: models.AdminBase, db: Session = Depends(get_db)):
    result = await crud.create_admin(req=req, db=db, header_param=header_param)
    if result:
        return Returns.object(result)
    else:
        return Returns.NOT_INSERTED


@authentication_router.put('/api/update-admin/{id}', dependencies=[Depends(HTTPBearer())])
async def update_admin(id: int, header_param: Request, req: models.AdminBase, db: Session = Depends(get_db)):
    result = await crud.update_admin(id=id, header_param=header_param, req=req, db=db)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED


@authentication_router.put('/api/delete-admin/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_admin(id: int, header_param: Request, req: models.AdminDelete, db: Session = Depends(get_db)):
    result = await crud.delete_admin(id=id, header_param=header_param, req=req, db=db)
    if result:
        return Returns.DELETED
    else:
        return Returns.NOT_DELETED


@authentication_router.put('/api/update-is-active/{id}', dependencies=[Depends(HTTPBearer())])
async def update_is_active(id: int, header_param: Request, req: models.AdminActiveSet, db: Session = Depends(get_db)):
    result = await crud.update_is_active(id=id, header_param=header_param, req=req, db=db)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED