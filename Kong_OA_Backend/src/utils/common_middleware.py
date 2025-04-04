import time

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from src.settings import setting
from src.utils.common_logger import logger


def add_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=setting.CORS_ALLOW_ORIGINS,
        allow_credentials=setting.CORS_ALLOW_CREDENTIALS,
        allow_methods=setting.CORS_ALLOW_METHODS,
        allow_headers=setting.CORS_ALLOW_HEADERS,
    )
    @app.middleware('http')
    async def visit_log(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time()
        total_time = str(end_time - start_time)
        logger.info(
            f"客户端ip: {request.client} 请求方式: {request.method} 请求路径: {request.url} 请求头: {request.headers}响应时间:{total_time}"
        )
        response.headers['X-Process-Time'] = total_time
        return response
