from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db import get_db
from returns import Returns
import models as mod
import crud


suborder_router = APIRouter()


@suborder_router.post('/api/create-suborder')
async def create_suborder(header_param: Request, req: mod.SuborderSchema, db: Session = Depends(get_db)):
    result = await crud.create_suborder(header_param, req, db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NOT_INSERTED



@suborder_router.put('/api/update-suborder/{id}')
async def update_suborder(id: int, header_param: Request, req: mod.SuborderSchema, db: Session = Depends(get_db)):
    result = await crud.update_suborder(id, header_param, req, db)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED


@suborder_router.get('/api/get-admin-suborder')
async def get_admin_suborder(header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_admin_suborder(header_param, db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
        