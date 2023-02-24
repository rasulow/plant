from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db import get_db
import crud
import models as mod

family_router = APIRouter(tags=['Family'])

@family_router.post('/api/create-family', dependencies=[Depends(HTTPBearer())])
async def create_family(header_param: Request, req: mod.FamilySchema, db: Session = Depends(get_db)):
    result = await crud.create_family(header_param=header_param, req=req, db=db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    


@family_router.put('/api/update-family/{id}', dependencies=[Depends(HTTPBearer())])
async def update_family(id: int, header_param: Request, req: mod.FamilySchema, db: Session = Depends(get_db)):
    result = await crud.update_family(id, header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Обновлено!'
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
@family_router.get('/api/get-admin-families')
async def get_admin_families(db: Session = Depends(get_db)):
    result = await crud.read_admin_family(db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    


@family_router.delete('/api/delete-family/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_family(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.delete_family(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@family_router.post('/api/create-family-synonym', dependencies=[Depends(HTTPBearer())])
async def create_family_synonym(header_param: Request, req: mod.FamilySynonymSchema, db: Session = Depends(get_db)):
    result = await crud.create_family_synonym(header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@family_router.delete('/api/delete-family-synonym/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_family_synonym(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.delete_family_synonym(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)