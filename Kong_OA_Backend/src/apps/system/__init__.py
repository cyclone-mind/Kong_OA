from .views.user import router as user_router
from .views.auth import router as auth_router

from fastapi import APIRouter

system_router = APIRouter()

system_router.include_router(user_router, prefix="/user", tags=["用户管理"])
system_router.include_router(auth_router, prefix="/auth", tags=["权限管理"])
