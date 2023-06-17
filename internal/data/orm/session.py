import typing as t
import logging

import pymysql
from pymysql import Connection
from dbutils.pooled_db import PooledDB

from internal.modules.utils import Singleton
from config import Config


class Define:
    Args = t.TypeVar('Args', t.List[t.Any], t.Dict[str, t.Any], t.Tuple[t.Any])


class DBException:
    """封装DB的异常"""

    class InternalErr(Exception):
        """DB内部异常"""


class DatabaseHandler(Singleton):
    """mysql handler"""
    def __init__(
            self,
            db_conf: t.Union[Config.DB, t.Dict] = None
    ):
        """init db pool"""
        if isinstance(db_conf, dict):
            self._conf = Config.DB(**db_conf)
        elif isinstance(db_conf, Config.DB):
            self._conf = db_conf
        else:
            self._conf = Config.DB()

        self._pool = PooledDB(
            creator=pymysql,
            maxconnections=1000,    # 连接池允许的最大连接数
            mincached=10,           # 初始化时, 连接池中最少创建的空闲连接, 0和None表示不限制
            maxcached=20,           # 连接池中最多的空闲连接, 0和None表示不限制
            maxshared=0,            # 连接池中最多共享的链接数量, 0和None表示全部共享
            blocking=True,          # 连接池中没有可用连接, 是否阻塞等待, True等待, False不等待, 报错
            maxusage=None,          # 一个连接最多被复用多少次, None表示无限制
            setsession=[],          # 开始会话执行前的命令列表
            # 0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created,
            # 4 = when a query is executed, 7 = always
            ping=0,
            host=self._conf.host,
            port=self._conf.port,
            user=self._conf.user,
            password=self._conf.password,
            database=self._conf.database,
            charset=self._conf.charset
        )

        self._conn: t.Optional[Connection] = None
        self._cur = None

    def open(self):
        self._conn = self._pool.connection()
        self._cur = self._conn.cursor(cursor=pymysql.cursors.DictCursor)
        return self

    def close(self):
        self._cur.close()
        self._conn.close()

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def execute(self, sql: str, args: Define.Args = None) -> int:
        return self._cur.execute(sql, args)

    def execute_all(self, sql: str, args: Define.Args = None) -> t.Tuple:
        self._cur.execute(sql, args)
        result = self._cur.fetchall()
        return result


class DBSession:
    def __init__(self, sess: DatabaseHandler, is_raise_err: bool = False):
        self._sess = sess.open()
        self._is_raise_err = is_raise_err

    def __enter__(self) -> DatabaseHandler:
        return self._sess

    def __exit__(self, exc_type, exc_val, exc_tb):
        # logging.info(f'type: {exc_type}, value: {exc_val}, traceback: {exc_tb}')
        try:
            self._sess.commit()
        except Exception as e:
            logging.error(e)
            self._sess.rollback()
            if self._is_raise_err:
                raise DBException.InternalErr
        finally:
            self._sess.close()


def new_database_handler(
        db_ep: str = None,
        db_auth: str = None,
        db_name: str = None,
        charset: str = None
) -> DatabaseHandler:
    """
    构造一个database handler对象
    :param db_ep: database endpoint, 格式: host:port
    :param db_auth: database auth: 格式: user:password
    :param db_name: database name
    :param charset: database charset
    :return: database handler
    """
    logging.info('start connect db...')
    conf = Config.DB()

    try:
        if db_ep:
            conf.host, conf.port = db_ep.split(':', 1)
            conf.port = int(conf.port)
        if db_auth:
            conf.user, conf.password = db_auth.split(':', 1)
        if db_name:
            conf.database = db_name
        if charset:
            conf.charset = charset
    except Exception as e:
        logging.error(e)
        return DatabaseHandler()

    logging.info(conf)

    return DatabaseHandler(conf)


# 初始化一个db的全局变量
db: t.Optional[DatabaseHandler] = None
