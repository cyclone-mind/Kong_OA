from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.settings import setting

DB_ORM_CONFIG = {
    "connections": {
        "default": {
            'engine': 'tortoise.backends.mysql',
            "credentials": {
                'host': setting.DB_HOST,
                'user': setting.DB_USER,
                'password': setting.DB_PASSWORD,
                'port': setting.DB_PORT,
                'database': setting.DB_DATABASE,
                'minsize': 1,
                'maxsize': 5,
                'charset': 'utf8mb4',
            }
        },

    },
    "apps": {
        'models': {
            'models': ['src.apps.system.models', 'src.apps.oa.models', "aerich.models"],  # aerich.models迁移模型
            'default_connection': 'default',
        }

    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}


def register_mysql(app: FastAPI):
    register_tortoise(app, config=DB_ORM_CONFIG)
