from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import Base, engine, get_db
from fastapi.middleware.cors import CORSMiddleware
from routers import authentication_router
from models import Users

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

app.include_router(authentication_router, tags=["Authentication"])
