import typing as t

from pydantic import BaseModel


ENV = 'local'


class ConfigInfo:

    ONE_DAY_IN_SECONDS = 60 * 60 * 24

    """服务配置信息"""
    class DB(BaseModel):
        host = '127.0.0.1'
        port = 3306
        user = 'root'
        password = '123456'
        database = 'token_system_db'
        charset = 'utf8mb4'

    class REDIS(BaseModel):
        host: str = 'localhost'
        port: int = 6379
        db: int = 3
        password: t.Optional[str] = None
        max_connections: int = 20
        decode_responses: bool = False


class LocalConfig(ConfigInfo):
    """本地配置"""


class DevelopmentConfig(ConfigInfo):
    """开发环境配置"""


class ProductionConfig(ConfigInfo):
    """正式环境配置"""


_config = {
    'default': LocalConfig,
    'local': LocalConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}


Config = _config[ENV]
