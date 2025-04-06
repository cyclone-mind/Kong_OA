from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
# 第一部分：自定义异常类
class LoginException(Exception):
    def __init__(self, code: int = None, msg: str = None):
        self.code = code
        self.msg = msg or '用户名或密码错误' or "已经被锁定"


class AuthException(Exception):
    def __init__(self, code: int = None, msg: str = None):
        self.code = code or 1001
        self.msg = msg or '用户认证失败'


class PermissionException(Exception):
    def __init__(self, code: int = None, msg: str = None):
        self.code = code or 1002
        self.msg = msg or '对不起，您没有权限操作'


class ServiceException(Exception):
    def __init__(self, code: int = None, msg: str = None):
        self.code = code or 1003
        self.msg = msg or '服务器异常，请稍后再试'


class ValidationException(Exception):
    def __init__(self, code: int = None, msg: str = None):
        self.code = code or 1004
        self.msg = msg or '数据校验异常'


# 2 注册异常

def register_exception(app: FastAPI):
    @app.exception_handler(AuthException)
    async def auth_exception_handler(request: Request, exc: AuthException):
        return JSONResponse(
            # status_code=exc.code,
            content={"code": exc.code, "msg": exc.msg},
        )
    @app.exception_handler(LoginException)
    async def login_exception_handler(request: Request, exc: LoginException):
        return JSONResponse(
            # status_code=exc.code,
            content={"code": exc.code, "msg": exc.msg},
        )
    @app.exception_handler(PermissionException)
    async def permission_exception_handler(request: Request, exc: PermissionException):
        return JSONResponse(
            # status_code=exc.code,
            content={"code": exc.code, "msg": exc.msg},
        )
    @app.exception_handler(ServiceException)
    async def service_exception_handler(request: Request, exc: ServiceException):
        return JSONResponse(
            # status_code=exc.code,
            content={"code": exc.code, "msg": exc.msg},
        )
    @app.exception_handler(ValidationException)
    async def validation_exception_handler(request: Request, exc: ValidationException):
        return JSONResponse(
            # status_code=exc.code,
            content={"code": exc.code, "msg": exc.msg},
        )

    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        return JSONResponse({'code': 1999, 'msg': f'服务器未知异常，请求稍后再试-【{str(exc)}】'})