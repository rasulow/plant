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


