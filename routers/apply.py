from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db import get_db
import crud
import models as mod


apply_router = APIRouter(tags=['Apply'], dependencies=[Depends(HTTPBearer())])


@apply_router.post('/api/create-apply')
async def create_apply(header_param: Request, req: mod.ApplySchema, db: Session = Depends(get_db)):
    result = await crud.create_apply(header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@apply_router.put('/api/update-apply/{id}')
async def update_apply(id: int, header_param: Request, req: mod.ApplySchema, db: Session = Depends(get_db)):
    result = await crud.update_apply(id, header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)