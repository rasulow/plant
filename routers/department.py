from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db import get_db
import crud
import models as mod
from returns import Returns


department_router = APIRouter()


@department_router.post('/api/create-department')
async def create_department(header_param: Request, req: mod.DepartmentSchema, db: Session = Depends(get_db)):
    result = await crud.create_department(header_param, req, db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NOT_INSERTED



@department_router.put('/api/update-department/{id}')
async def update_department(id: int, header_param: Request, req: mod.DepartmentSchema, db: Session = Depends(get_db)):
    result = await crud.update_department(id, header_param, req, db)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED


@department_router.get('/api/get-admin-departments')
async def get_admin_departments(header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_admin_departments(header_param, db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL