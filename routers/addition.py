from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db import get_db
import crud
import models as mod


addition_router = APIRouter(tags=['Addition'], dependencies=[Depends(HTTPBearer())])

@addition_router.post('/api/create-addition')
async def create_addition(header_param: Request, req: mod.AdditionSchema, db: Session = Depends(get_db)):
    result = await crud.create_addition(header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@addition_router.put('/api/update-addition/{id}')
async def update_addition(id: int, header_param: Request, req: mod.AdditionSchema, db: Session = Depends(get_db)):
    result = await crud.update_addition(id, header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)