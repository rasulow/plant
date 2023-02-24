from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db import get_db
import crud
import models as mod


plant_router = APIRouter(tags=['Plant'])



@plant_router.post('/api/create-plant', dependencies=[Depends(HTTPBearer())])
async def create_plant(header_param: Request, req: mod.PlantSchema, db: Session = Depends(get_db)):
    result = await crud.create_plant(header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        print(result.id)
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@plant_router.put('/api/update-plant/{id}', dependencies=[Depends(HTTPBearer())])
async def update_plant(id: int, header_param: Request, req: mod.PlantSchemaUpdate, db: Session = Depends(get_db)):
    result = await crud.update_plant(id, header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
@plant_router.get('/api/get-admin-plant')
async def get_admin_plant(db: Session = Depends(get_db)):
    result = await crud.read_admin_plant(db)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
@plant_router.get('/api/get-admin-plant-by-id/{id}')
async def get_admin_plant_by_id(id: int, db: Session = Depends(get_db)):
    result = await crud.read_admin_plant_by_id(id, db)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
@plant_router.delete('/api/delete-plant/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_plant(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.delete_plant(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
#################################################################################################


@plant_router.post('/api/create-fullname-synonym', dependencies=[Depends(HTTPBearer())])
async def create_fullname_synonym(header_param: Request, req: mod.FullnameSynonymCreateSchema, db: Session = Depends(get_db)):
    result = await crud.create_fullname_synonym(header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@plant_router.delete('/api/delete-fullname-synonym/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_fullname_synonym(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.delete_fullname_synonym(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    

@plant_router.post('/api/create-link-synonym', dependencies=[Depends(HTTPBearer())])
async def create_link_synonym(header_param: Request, req: mod.LinkSynonymCreateSchema, db: Session = Depends(get_db)):
    result = await crud.create_link_synonym(header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@plant_router.delete('/api/delete-link-synonym/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_link_synonym(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.delete_link_synonym(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
@plant_router.post('/api/create-plant-author', dependencies=[Depends(HTTPBearer())])
async def create_plant_author(header_param: Request, req: mod.PlantAuthorCreateSchema, db: Session = Depends(get_db)):
    result = await crud.create_plant_author(header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@plant_router.delete('/api/delete-plant-author/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_plant_author(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.delete_plant_author(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)