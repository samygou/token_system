import typing as t
import uuid

import redis
from zope.interface import implementer

from internal.modules.utils import Singleton
from internal.modules import lockx


_MAX_CONNECTIONS = 20


class Client(Singleton):
    """"""
    def __init__(
            self,
            host: str,
            port: int,
            password: str = None,
            db: int = 0,
            max_connections: int = 20,
            decode_responses: bool = True
    ):
        """

        :param host:
        :param port:
        :param password:
        :param db:
        :param max_connections:
        :param decode_responses:
        """
        host = host if host else 'localhost'
        port = port if port else 6379
        self._pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
            max_connections=max_connections,
            decode_responses=decode_responses
        )
        self.cli = redis.StrictRedis(connection_pool=self._pool)

    def ping(self) -> bool:
        """"""
        return self.cli.ping()

    def keep_alive(self):
        """

        :return:
        """

    def lock(self, lock_name: str, ttl: int = 60):
        """

        :param lock_name:
        :param ttl:
        :return:
        """
        return Lock(lock_name, ttl, client=self)


def new_client(
        host: str,
        port: int,
        db: int = 0,
        password: str = None,
        max_connections: int = _MAX_CONNECTIONS,
        decode_responses: bool = False
) -> Client:
    """

    :param host:
    :param port:
    :param db:
    :param password:
    :param max_connections:
    :param decode_responses:
    :return:
    """
    return Client(
        host=host,
        port=port,
        db=db,
        password=password,
        max_connections=max_connections,
        decode_responses=decode_responses
    )


@implementer(lockx.ILock)
class Lock:
    """
    分布式锁
    """
    def __init__(
            self,
            name: str = None,
            ttl: int = 60,
            client: t.Optional[Client] = None
    ):
        """

        :param name: name设置为可选值, 为了使用对象池模式
        :param ttl: 锁超时时间
        """
        self._name = name
        self._val = uuid.uuid4().bytes
        self._ttl = ttl
        self.redis_cli = client

    def init(self, name: str, ttl: int = 60):
        self._name = name
        self._ttl = ttl
        self._val = uuid.uuid4().bytes

    def acquire(self):
        if self.redis_cli.cli.set(self._name, self._val, ex=self._ttl, nx=True):
            if self.redis_cli.cli.ttl(self._name) == -1:
                self.redis_cli.cli.expire(self._name, self._ttl)

            return True

        return False

    def release(self):
        self.redis_cli.cli.delete(self._name)

    def is_acquired(self) -> bool:
        val = self.redis_cli.cli.get(self._name)

        if not val:
            return False

        return val == self._val

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
