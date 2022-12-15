from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db import get_db
import crud
import models
from returns import Returns

class_router = APIRouter()

