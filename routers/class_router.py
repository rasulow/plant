from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db import get_db
import crud
import models as mod
from returns import Returns

class_router = APIRouter(tags=['Class'])


@class_router.post('/api/create-class')
async def create_class(req: mod.ClassSchema, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.create_class(req, header_param, db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@class_router.put('/api/update-class/{id}')
async def update_class(id: int, header_param: Request, req: mod.ClassSchema, db: Session = Depends(get_db)):
    result = await crud.update_class(id, header_param, req, db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)



@class_router.get('/api/get-admin-classes')
async def get_admin_classes(header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_admin_classes(header_param, db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)



