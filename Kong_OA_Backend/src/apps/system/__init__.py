from .views.user import router as user_router
from .views.auth import router as auth_router
from .views.dept import router as dept_router
from .views.job import router as job_router
from .views.role import router as role_router
from .views.menu import router as menu_router

from fastapi import APIRouter

system_router = APIRouter()

system_router.include_router(auth_router, prefix="/auth", tags=["权限管理"])
system_router.include_router(user_router, prefix="/user", tags=["用户管理"])
system_router.include_router(dept_router, prefix="/dept", tags=["部门管理"])
system_router.include_router(job_router, prefix="/job", tags=["岗位管理"])
system_router.include_router(role_router, prefix="/role", tags=["角色管理"])
system_router.include_router(menu_router, prefix="/menu", tags=["菜单管理"])
