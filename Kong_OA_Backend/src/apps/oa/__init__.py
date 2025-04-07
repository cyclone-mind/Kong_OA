from .views import router as leave_router
from fastapi import APIRouter

oa_router = APIRouter()

oa_router.include_router(leave_router, prefix='/leave', tags=['请假所有的路由'])
