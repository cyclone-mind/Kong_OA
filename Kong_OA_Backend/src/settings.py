# 导入dotenv模块中的load_dotenv函数，用于加载环境变量
from dotenv import load_dotenv
# 导入pydantic_settings模块中的BaseSettings类，用于定义和验证配置设置
from pydantic_settings import BaseSettings
# 导入pathlib模块中的Path类，用于处理文件路径
from pathlib import Path


class APPConfigSettings(BaseSettings):
    """
    APPConfigSettings类用于定义和验证应用程序的配置设置。

    Attributes:
        APP_HOST (str): 应用程序的主机地址。
        APP_PORT (int): 应用程序的端口号。
        BASE_DIR (Path): 应用程序的基础目录。
    """
    # 加载环境变量
    load_dotenv()
    # 应用程序的主机地址，类型为字符串
    APP_HOST: str
    # 应用程序的端口号，类型为整数
    APP_PORT: int
    # 应用程序的基础目录，类型为Path，默认值为当前文件的父目录的父目录
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # 允许跨域请求的来源列表
    CORS_ALLOW_ORIGINS: list = ["*"]

    # 是否允许跨域请求携带用户凭证
    CORS_ALLOW_CREDENTIALS: bool = True

    # 允许跨域请求的方法列表
    CORS_ALLOW_METHODS: list = ["*"]

    # 允许跨域请求的头部列表
    CORS_ALLOW_HEADERS: list = ["*"]

    # MYSQL 相关
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: str
    DB_DATABASE: str = "kong_oa"


    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24*7
    SECRET_KEY: str = ("KONAD_555")
    ALGORITHM: str = "HS256"


# 创建APPConfigSettings类的实例，用于获取应用程序的配置设置
setting = APPConfigSettings()

if __name__ == '__main__':
    print(setting.BASE_DIR.joinpath('logs'))
    print(type(setting.BASE_DIR.joinpath('logs')))