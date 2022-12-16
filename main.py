from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    department_router,
    authentication_router,
    class_router,
    subclass_router,
    supersubclass_router
)
from db import Base, engine


app = FastAPI(title='Plant API')

origins = ["*"]
methods = ["*"]
headers = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
)

Base.metadata.create_all(engine)

app.include_router(authentication_router    , tags=["Authentication"])
app.include_router(department_router        , tags=['Department']       , dependencies=[Depends(HTTPBearer())])
app.include_router(class_router             , tags=['Class']            , dependencies=[Depends(HTTPBearer())])
app.include_router(subclass_router          , tags=['Subclass']         , dependencies=[Depends(HTTPBearer())])
app.include_router(supersubclass_router     , tags=['Supersubclass']    , dependencies=[Depends(HTTPBearer())])