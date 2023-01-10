from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db import get_db
import models as mod
import crud


order_router = APIRouter(tags=['Order'], dependencies=[Depends(HTTPBearer())])

@order_router.post('/api/create-order')
async def create_order(header_param: Request, req: mod.OrderSchema, db: Session = Depends(get_db)):
    result = await crud.create_order(header_param, req, db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@order_router.put('/api/update-order/{id}')
async def update_order(id: int, header_param: Request, req: mod.OrderSchema, db: Session = Depends(get_db)):
    result = await crud.update_order(id, header_param, req, db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@order_router.get('/api/get-admin-order')
async def create_order(header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_admin_order(header_param, db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)