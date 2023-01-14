from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db import get_db
import crud
import models as mod


genus_router = APIRouter(tags=['Genus'], dependencies=[Depends(HTTPBearer())])


@genus_router.post('/api/create-genus')
async def create_genus(header_param: Request, req: mod.GenusSchema, db: Session = Depends(get_db)):
    result = await crud.create_genus(header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
        


@genus_router.put('/api/update-genus/{id}')
async def update_genus(id: int, header_param: Request, req: mod.GenusSchema, db: Session = Depends(get_db)):
    result = await crud.update_genus(id, header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@genus_router.get('/api/get-admin-genus')
async def get_admin_genus(header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_admin_genus(header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
@genus_router.delete('/api/delete-genus/{id}')
async def delete_genus(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.delete_genus(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
@genus_router.post('/api/create-genus-synonym')
async def create_genus_synonym(header_param: Request, req: mod.GenusSynonymSchema, db: Session = Depends(get_db)):
    result = await crud.create_genus_synonym(header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
@genus_router.delete('/api/delete-genus-synonym/{id}')
async def delete_genus_synonym(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.delete_genus_synonym(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)