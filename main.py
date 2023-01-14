from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    department_router,
    authentication_router,
    class_router,
    subclass_router,
    supersubclass_router,
    order_router,
    suborder_router,
    family_router,
    genus_router,
    plant_router
)
from db import Base, engine


app = FastAPI(title='Plant Cadastre API')

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

app.include_router(authentication_router)
app.include_router(department_router)
app.include_router(class_router)
app.include_router(subclass_router)
app.include_router(supersubclass_router)
app.include_router(order_router)
app.include_router(suborder_router)
app.include_router(family_router)
app.include_router(genus_router)
app.include_router(plant_router)