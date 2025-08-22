from fastapi import APIRouter
from .authRouter import auth_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/v1", tags=["auth"])