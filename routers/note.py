from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db import get_db
import crud
import models as mod


note_router = APIRouter(tags=['Note'], dependencies=[Depends(HTTPBearer())])


@note_router.post('/api/create-note')
async def create_note(header_param: Request, req: mod.NoteSchema, db: Session = Depends(get_db)):
    result = await crud.create_note(header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@note_router.put('/api/update-note/{id}')
async def update_note(id: int, header_param: Request, req: mod.NoteSchema, db: Session = Depends(get_db)):
    result = await crud.update_note(id, header_param, req, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@note_router.delete('/api/delete-note/{id}')
async def delete_note(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.delete_note(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)