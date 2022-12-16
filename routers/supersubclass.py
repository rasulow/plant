from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db import get_db
import crud
import models as mod
from returns import Returns

supersubclass_router = APIRouter()


@supersubclass_router.post('/api/create-supersubclass')
async def create_supersubclass(header_param: Request, req: mod.SupersubclassSchema, db: Session = Depends(get_db)):
    result = await crud.create_supersubclass(header_param, req, db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NOT_INSERTED


@supersubclass_router.put('/api/update-supersubclass/{id}')
async def update_supersubclass(id: int, header_param: Request, req: mod.SupersubclassSchema, db: Session = Depends(get_db)):
    result = await crud.update_supersubclass(id, header_param, req, db)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED



@supersubclass_router.get('/api/get-admin-supersubclass')
async def get_admin_supersubclass(header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_admin_supersubclass(header_param, db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL