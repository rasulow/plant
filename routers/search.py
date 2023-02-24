from fastapi import APIRouter, Depends, Request, status, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db import get_db
import crud
import models as mod
from typing import List, Optional

search_router = APIRouter(tags=['Search'])

@search_router.get('/api/search-admin')
async def get_search(
    department_id   : Optional[str] = Query(None),
    class_id        : Optional[str] = Query(None),
    subclass_id     : Optional[str] = Query(None),
    supersubclass_id: Optional[str] = Query(None),
    order_id        : Optional[str] = Query(None),
    suborder_id     : Optional[str] = Query(None),
    family_id       : Optional[str] = Query(None),
    genus_id        : Optional[str] = Query(None),
    text            : Optional[str] = Query(None),
    db              : Session = Depends(get_db)
):
    result = await crud.search_admin(
        department_id,   
        class_id,        
        subclass_id,     
        supersubclass_id,
        order_id,        
        suborder_id,     
        family_id,       
        genus_id,        
        text,            
        db
    )
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)