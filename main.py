from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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
    plant_router,
    areal_router,
    morphology_router,
    ecology_router,
    note_router,
    apply_router,
    addition_router,
    map_router,
    image_router,
    herbarium_router,
    search_router
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


app.mount('/uploads', StaticFiles(directory="uploads"), name="uploads")


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
app.include_router(areal_router)
app.include_router(morphology_router)
app.include_router(ecology_router)
app.include_router(note_router)
app.include_router(apply_router)
app.include_router(addition_router)
app.include_router(map_router)
app.include_router(image_router)
app.include_router(herbarium_router)
app.include_router(search_router)