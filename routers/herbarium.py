from fastapi import APIRouter, Depends, Request, status, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db import get_db
import crud
import models as mod


herbarium_router = APIRouter(tags=['Herbarium'], dependencies=[Depends(HTTPBearer())])


@herbarium_router.post('/api/create-herbarium')
async def create_herbarium(header_param: Request, req: mod.HerbariumSchema, db: Session = Depends(get_db)):
    result = await crud.create_herbarium(header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
    
@herbarium_router.put('/api/update-herbarium-image/{id}')
async def update_herbarium_image(id: int, header_param: Request, db: Session = Depends(get_db), file: UploadFile = File(...)):
    result = await crud.update_herbarium_image(id, header_param, db, file)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
    
@herbarium_router.delete('/api/delete-herbarium/{id}')
async def delete_herbarium(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.delete_herbarium(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@herbarium_router.get('/api/get-herbarium/{plant_id}')
async def get_herbarium(plant_id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_herbarium(plant_id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)