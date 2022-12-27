from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db import get_db
from returns import Returns
import models as mod
import crud


order_router = APIRouter()

@order_router.post('/api/create-order')
async def create_order(header_param: Request, req: mod.OrderSchema, db: Session = Depends(get_db)):
    result = await crud.create_order(header_param, req, db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NOT_INSERTED


@order_router.put('/api/update-order/{id}')
async def update_order(id: int, header_param: Request, req: mod.OrderSchema, db: Session = Depends(get_db)):
    result = await crud.update_order(id, header_param, req, db)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED


@order_router.get('/api/get-admin-order')
async def create_order(header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_admin_order(header_param, db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL