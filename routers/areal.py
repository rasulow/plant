from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db import get_db
import crud
import models as mod


areal_router = APIRouter(tags=['Areals'], dependencies=[Depends(HTTPBearer())])

@areal_router.post('/api/create-areal')
async def create_areal(header_param: Request, req: mod.ArealSchema, db: Session = Depends(get_db)):
    result = await crud.create_areals(header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
@areal_router.get('/api/get-areal/{id}')
async def get_areal(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_areal(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@areal_router.put('/api/update-areal/{id}')
async def update_areal(id: int, header_param: Request, req: mod.ArealSchema, db: Session = Depends(get_db)):
    result = await crud.update_areal(id, header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@areal_router.delete('/api/delete-areal/{id}')
async def delete_areal(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.delete_areal(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


