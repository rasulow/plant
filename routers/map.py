from fastapi import APIRouter, Depends, Request, status, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db import get_db
import crud
import models as mod


map_router = APIRouter(tags=['Map'], dependencies=[Depends(HTTPBearer())])


@map_router.post('/api/create-map/{plant_id}')
async def create_map(plant_id: int, header_param: Request, db: Session = Depends(get_db), file: UploadFile = File(...)):
    print(file.filename)
    result = await crud.create_map(plant_id, header_param, db, file)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
