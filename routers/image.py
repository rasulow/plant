from fastapi import APIRouter, Depends, Request, status, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db import get_db
import crud
import models as mod


image_router = APIRouter(tags=['Image'], dependencies=[Depends(HTTPBearer())])


@image_router.post('/api/create-image/{plant_id}')
async def create_image(plant_id: int, header_param: Request, db: Session = Depends(get_db), file: UploadFile = File(...)):
    result = await crud.create_image(plant_id, header_param, db, file)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result == -2:
        result = {'msg': 'Вы не можете добавлять больше 6 картинок!!!'}
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@image_router.get('/api/get-image/{plant_id}')
async def get_image(plant_id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_image(plant_id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@image_router.delete('/api/delete-image/{id}')
async def delete_image(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.delete_image(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
