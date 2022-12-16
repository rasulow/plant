from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db import get_db
import crud
import models as mod
from returns import Returns

subclass_router = APIRouter()


@subclass_router.post('/api/create-subclass')
async def create_subclass(header_param: Request, req: mod.SubclassSchema, db: Session = Depends(get_db)):
    result = await crud.create_subclass(header_param, req, db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NOT_INSERTED


@subclass_router.put('/api/update-subclass/{id}')
async def update_subclass(id: int, header_param: Request, req: mod.SubclassSchema, db: Session = Depends(get_db)):
    result = await crud.update_subclass(id, header_param, req, db)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED


@subclass_router.get('/api/get-admin-subclass')
async def get_admin_subclass(header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_admin_subclass(header_param, db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL