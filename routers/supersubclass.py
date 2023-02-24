from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db import get_db
import crud
import models as mod
from returns import Returns

supersubclass_router = APIRouter(tags=['Supersubclass'])


@supersubclass_router.post('/api/create-supersubclass', dependencies=[Depends(HTTPBearer())])
async def create_supersubclass(header_param: Request, req: mod.SupersubclassSchema, db: Session = Depends(get_db)):
    result = await crud.create_supersubclass(header_param, req, db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@supersubclass_router.put('/api/update-supersubclass/{id}', dependencies=[Depends(HTTPBearer())])
async def update_supersubclass(id: int, header_param: Request, req: mod.SupersubclassSchema, db: Session = Depends(get_db)):
    result = await crud.update_supersubclass(id, header_param, req, db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)



@supersubclass_router.get('/api/get-admin-supersubclass')
async def get_admin_supersubclass(db: Session = Depends(get_db)):
    result = await crud.read_admin_supersubclass(db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)