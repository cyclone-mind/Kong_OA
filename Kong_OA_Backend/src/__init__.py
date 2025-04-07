from fastapi import FastAPI
from src.apps.home import home_router
from src.apps.system import system_router
from src.apps.oa import oa_router
from src.utils.common_middleware import add_cors_middleware
from src.utils.common_db import register_mysql
from src.utils.common_exception import register_exception
from fastapi.staticfiles import StaticFiles


def register_router(app: FastAPI):
    # http://127.0.0.1:8000/api/v1/home/main
    # http://127.0.0.1:8000/api/v1/system/user
    app.include_router(home_router, prefix='/api/v1/home', tags=['首页所有的路由'])
    app.include_router(system_router, prefix='/api/v1/system', tags=['系统所有的路由'])
    app.include_router(oa_router, prefix='/api/v1/oa', tags=['oa所有的路由'])


def register_middleware(app: FastAPI):
    add_cors_middleware(app)


def create_app() -> FastAPI:
    # 1 实例化得到app对象
    app = FastAPI()
    # 2 注册路由,并分发
    register_router(app)
    # 3 注册中间件
    register_middleware(app)
    # 4 注册ORM
    register_mysql(app)
    # 5 注册全局异常
    register_exception(app)
    # 6 开启media访问
    app.mount("/media", StaticFiles(directory="media"), name="media")
    return app
