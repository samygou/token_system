import typing as t
import queue

from zope.interface import Interface

from internal.modules.utils import NoException


class ILock(Interface):
    """Distributed lock interface"""

    def init(self, name: str, ttl: int = 60):
        """对象池模式重新初始化对象"""

    def acquire(self) -> bool:
        """acquire lock"""

    def release(self):
        """release lock"""

    def is_acquired(self) -> bool:
        """is acquired lock"""


class Lock:
    """"""
    def __init__(
            self,
            cli: ILock,
            name: t.Optional[str] = None,
            ttl: int = 60
    ):
        """
        初始化分布式锁, 目前可选择redis和etcd
        注: with 上下文模式慎用, 如果是大量线程同时获取锁的时候, 会不断的加锁 -> 释放锁, 因为退出with的时候会自动释放锁
        :param cli: 锁客户端
        :param name: lock name
        :param ttl: lock expired, seconds
        """
        self._cli = cli
        self._name = name
        self._ttl = ttl

    @property
    def name(self):
        return self._name

    @property
    def ttl(self):
        return self._ttl

    @name.setter
    def name(self, _name: str):
        self._name = _name

    @ttl.setter
    def ttl(self, _ttl: int):
        self._ttl = _ttl

    def init(self, name: str, ttl: int = 60):
        self._cli.init(name, ttl)

    @NoException()
    def acquire(self) -> bool:
        """
        acquire lock, etcd retry raise Exception, catch it and do not raise
        :return:
        """
        return self._cli.acquire()

    @NoException()
    def release(self):
        """
        release lock
        :return:
        """
        self._cli.release()

    @NoException()
    def is_acquired(self) -> bool:
        """判断是否是自己家的锁"""
        return self._cli.is_acquired()

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


class LockPool:
    """lock对象池"""
    def __init__(self, pool: int, timeout: int = 5):
        self._pool = queue.Queue(pool)
        self._timeout = timeout

    def get(self):
        return self._pool.get(timeout=self._timeout)

    def put(self, lock_cli: Lock):
        self._pool.put(lock_cli, timeout=self._timeout)
