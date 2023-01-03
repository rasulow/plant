from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db import get_db
from returns import Returns
import models as mod
import crud


suborder_router = APIRouter()


@suborder_router.post('/api/create-suborder')
async def create_suborder(header_param: Request, req: mod.SuborderSchema, db: Session = Depends(get_db)):
    result = await crud.create_suborder(header_param, req, db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)



@suborder_router.put('/api/update-suborder/{id}')
async def update_suborder(id: int, header_param: Request, req: mod.SuborderSchema, db: Session = Depends(get_db)):
    result = await crud.update_suborder(id, header_param, req, db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@suborder_router.get('/api/get-admin-suborder')
async def get_admin_suborder(header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_admin_suborder(header_param, db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
        