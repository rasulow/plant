from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db import get_db
import crud
import models as mod


morphology_router = APIRouter(tags=['Morphology'])



@morphology_router.post('/api/create-morphology', dependencies=[Depends(HTTPBearer())])
async def create_morphology(header_param: Request, req: mod.MorphologySchema, db: Session = Depends(get_db)):
    result = await crud.create_morphology(header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
@morphology_router.get('/api/get-morphology/{id}')
async def get_morphology(id: int, db: Session = Depends(get_db)):
    result = await crud.read_morphology(id, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@morphology_router.put('/api/update-morphology/{id}', dependencies=[Depends(HTTPBearer())])
async def update_morphology(id: int, header_param: Request, req: mod.MorphologySchema, db: Session = Depends(get_db)):
    result = await crud.update_morphology(id, header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@morphology_router.delete('/api/delete-morphology/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_morphology(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.delete_morphology(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)