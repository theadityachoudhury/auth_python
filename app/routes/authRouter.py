from fastapi import APIRouter, status
from app.schemas.users import UserCreate, UserResponse
from app.controllers.user_controller import user_controller

auth_router = APIRouter(
    prefix="/auth", 
    tags=["auth"]
)

@auth_router.post("/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user account with the provided information.")
async def create_user(user_data: UserCreate):
    return await user_controller.create_user(user_data)

@auth_router.get("/login")
async def login():
    """
    Endpoint for user login.
    """
    return {"message": "Login endpoint"}