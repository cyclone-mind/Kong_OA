from fastapi import APIRouter
from fastapi.requests import Request
from starlette.responses import JSONResponse

from src.utils.common_logger import logger
from src.utils.common_exception import AuthException

router = APIRouter()


# @router.get("/info")
# async def get_info():
#     return {"msg": "hello world"}


@router.get("/logger_demo")
async def logger_demo(request: Request):
    # 用户一进来就打印info日志
    logger.info("来了老弟？")
    # 除了异常就打印error日志
    try:
        1 / 0
    except Exception as e:
        logger.error(f'出错了，错误是：{str(e)}')
    return {"msg": "logger demo"}


@router.get("/exception_demo")
async def exception_demo(request: Request):
    # raise AuthException(msg='用户认证失败')
    # l=[1,2,3]
    # print(l[9])
    return "demo"

from src.utils.common_response import APIResponse
@router.get('/info')
async def cpu_demo(request: Request):
    # 取出cpu核数和cpu占用率--返回
    import psutil
    def get_os_info():
        import platform
        return platform.system()+"=="+platform.release()
    def get_cpu_info():
        return {
            "percent":psutil.cpu_percent(interval=1),
            "count":psutil.cpu_percent()
        }
    def get_disk_info():
        disk_usage = psutil.disk_usage('/')
        return {
            "total":disk_usage.total / (1024.0 ** 3 ),
            "used":disk_usage.used / (1024.0 ** 3 ),
            "free":disk_usage.free / (1024.0 ** 3 ),
            "percent":disk_usage.percent
        }

    def get_memory_info():
        mem = psutil.virtual_memory()
        return {
            "total":mem.total / (1024.0 ** 3 ),
            "used":mem.used / (1024.0 ** 3 ),
            "free":mem.free / (1024.0 ** 3 ),
            "percent":mem.percent
        }

    def get_network_info():
        net = psutil.net_io_counters()
        return {
            "sent_packets":net.packets_sent,
            "recv_packets":net.packets_recv,
        }
    system_info = {
        "os":get_os_info(),
        "cpu":get_cpu_info(),
        "disk":get_disk_info(),
        "memory":get_memory_info(),
        "network":get_network_info()
        }
    return  APIResponse(data=system_info)
    # return JSONResponse({'code':100,'msg':'请求成功','data':{'cpu_count': cpu_count, 'cpu_percent': cpu_percent}})
    # return APIResponse(data={'cpu_count': cpu_count, 'cpu_percent': cpu_percent})