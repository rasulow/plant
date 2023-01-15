from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db import get_db
import crud
import models as mod
from returns import Returns

subclass_router = APIRouter(tags=['Subclass'], dependencies=[Depends(HTTPBearer())])


@subclass_router.post('/api/create-subclass')
async def create_subclass(header_param: Request, req: mod.SubclassSchema, db: Session = Depends(get_db)):
    result = await crud.create_subclass(header_param, req, db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@subclass_router.put('/api/update-subclass/{id}')
async def update_subclass(id: int, header_param: Request, req: mod.SubclassSchema, db: Session = Depends(get_db)):
    result = await crud.update_subclass(id, header_param, req, db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@subclass_router.get('/api/get-admin-subclass')
async def get_admin_subclass(header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_admin_subclass(header_param, db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)