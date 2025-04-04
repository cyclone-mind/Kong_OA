import time
from loguru import logger
from src.settings import setting


def get_logger():
    # 1 判断logs文件夹是否存在，如果不存在，就创建
    # 构建日志文件的路径，将项目根目录与 'logs' 文件夹拼接
    log_path = setting.BASE_DIR.joinpath('logs')
    # 创建日志文件夹，如果文件夹已存在则不会引发错误
    log_path.mkdir(parents=True, exist_ok=True)
    # 2 设置info级别和error级别日志文件，放在不同文件中
    # 设置info级别和error级别的日志文件
    log_path_info = log_path.joinpath(f"info_{time.strftime('%Y-%m-%d')}.log")
    log_path_error = log_path.joinpath(f"error_{time.strftime('%Y-%m-%d')}.log")
    # 3 设置info级别和error级别日志格式
    # 设置info级别和error级别的日志格式
    log_format_info = '{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name}:{function}:{line} | {message}'
    log_format_error = '{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name}:{function}:{line} | {message} | {exception}'

    # 4 设置info级别和error级别的日志输出格式
    # 设置info级别和error级别的日志输出格式
    logger.add(
        log_path_info,
        format=log_format_info,
        level='INFO',
        rotation='00:00',
        retention='7 days',
        encoding='utf-8'
    )
    logger.add(
        log_path_error,
        format=log_format_error,
        level='ERROR',
        rotation='500 MB',
        retention='4 weeks',
        encoding='utf-8',
        mode='a+'
    )
    return logger

get_logger()

if __name__ == '__main__':
    logger.info('info')
    logger.error('error')
