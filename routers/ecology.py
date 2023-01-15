from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db import get_db
import crud
import models as mod


ecology_router = APIRouter(tags=['Ecology'], dependencies=[Depends(HTTPBearer())])


@ecology_router.post('/api/create-ecology')
async def create_ecology(header_param: Request, req: mod.EcologySchema, db: Session = Depends(get_db)):
    result = await crud.create_ecology(header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@ecology_router.put('/api/update-ecology/{id}')
async def update_ecology(id: int, header_param: Request, req: mod.EcologySchema, db: Session = Depends(get_db)):
    result = await crud.update_ecology(id, header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@ecology_router.delete('/api/delete-ecology/{id}')
async def delete_ecology(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.delete_ecology(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)