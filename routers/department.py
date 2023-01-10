from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db import get_db
import crud
import models as mod


department_router = APIRouter(tags=['Department'], dependencies=[Depends(HTTPBearer())])


@department_router.post('/api/create-department')
async def create_department(header_param: Request, req: mod.DepartmentSchema, db: Session = Depends(get_db)):
    result = await crud.create_department(header_param, req, db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)



@department_router.put('/api/update-department/{id}')
async def update_department(id: int, header_param: Request, req: mod.DepartmentSchema, db: Session = Depends(get_db)):
    result = await crud.update_department(id, header_param, req, db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@department_router.get('/api/get-admin-departments')
async def get_admin_departments(header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_admin_departments(header_param, db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)