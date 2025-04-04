from .views.views import router as main_router
from fastapi import APIRouter

# 创建一个名为home_router的APIRouter实例，用于定义与首页相关的路由
home_router = APIRouter()

# 将main_router包含在home_router中，并设置前缀为"/main"，标签为["首页核心接口"]
# 这样，main_router中定义的所有路由都将以"/main"为前缀，并且在API文档中显示为"首页核心接口"
home_router.include_router(main_router, prefix="/main", tags=["首页核心接口"])
