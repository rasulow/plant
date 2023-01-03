from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
import crud
import models as mod
from returns import Returns


authentication_router = APIRouter()



########################
# ADMIN AUTHENTICATION #
########################


@authentication_router.post('/api/login-admin')
async def login_admin(req: mod.LoginSchema, db: Session = Depends(get_db)):
    result = await crud.admin_login(req, db)
    result = jsonable_encoder(result)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username or Password wrong')


@authentication_router.post('/api/login-user')
async def login_user(req: mod.LoginSchema, db: Session = Depends(get_db)):
    result = await crud.user_login(req, db)
    result = jsonable_encoder(result)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username or Password wrong')


@authentication_router.post('/api/create-superadmin')
async def create_superadmin(db: Session = Depends(get_db)):
    result = await crud.create_superadmin(db=db)
    result = jsonable_encoder(result)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)



@authentication_router.get('/api/get-users', dependencies=[Depends(HTTPBearer())])
async def get_users(header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_all_users(header_param = header_param, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@authentication_router.get('/api/get-user/{id}', dependencies=[Depends(HTTPBearer())])
async def get_user(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_user(id=id, header_param=header_param, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@authentication_router.get('/api/get-admins', dependencies=[Depends(HTTPBearer())])
async def get_admins(header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_all_admins(header_param=header_param, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@authentication_router.get('/api/get-admin/{id}', dependencies=[Depends(HTTPBearer())])
async def get_admin(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.read_admin(id=id, header_param=header_param, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@authentication_router.post('/api/create-admin', dependencies=[Depends(HTTPBearer())])
async def create_admin(header_param: Request, req: mod.AdminBase, db: Session = Depends(get_db)):
    result = await crud.create_admin(req=req, db=db, header_param=header_param)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@authentication_router.put('/api/update-admin/{id}', dependencies=[Depends(HTTPBearer())])
async def update_admin(id: int, header_param: Request, req: mod.AdminBase, db: Session = Depends(get_db)):
    result = await crud.update_admin(id=id, header_param=header_param, req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@authentication_router.put('/api/delete-admin/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_admin(id: int, header_param: Request, req: mod.UserDelete, db: Session = Depends(get_db)):
    result = await crud.delete_admin(id=id, header_param=header_param, req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@authentication_router.put('/api/update-admin-is-active/{id}', dependencies=[Depends(HTTPBearer())])
async def update_is_active(id: int, header_param: Request, req: mod.UserActiveSet, db: Session = Depends(get_db)):
    result = await crud.update_admin_is_active(id=id, header_param=header_param, req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)





#######################
# USER AUTHENTICATION #
#######################




@authentication_router.post('/api/create-user', dependencies=[Depends(HTTPBearer())])
async def create_user(header_param: Request, req: mod.UserBase, db: Session = Depends(get_db)):
    result = await crud.create_user(header_param=header_param, req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)



@authentication_router.put('/api/update-user/{id}', dependencies=[Depends(HTTPBearer())])
async def update_user(id: int, header_param: Request, req: mod.UserBase, db: Session = Depends(get_db)):
    result = await crud.update_user(id=id, header_param=header_param, req=req, db=db)
    print(result)
    result = jsonable_encoder(result)
    print(result)
    
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)



@authentication_router.put('/api/delete-user/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_user(id: int, header_param: Request, req: mod.UserDelete, db: Session = Depends(get_db)):
    result = await crud.delete_user(id=id, header_param=header_param, req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@authentication_router.put('/api/update-user-is-active/{id}', dependencies=[Depends(HTTPBearer())])
async def update_user_is_active(id: int, header_param: Request, req: mod.UserActiveSet, db: Session = Depends(get_db)):
    result = await crud.update_user_is_active(id=id, header_param=header_param, req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
