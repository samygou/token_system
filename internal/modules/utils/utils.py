import threading
import functools
import logging
import traceback
import typing as t


class MakeSynchronized:
    def __init__(self):
        self._lock = threading.Lock()

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with self._lock:
                return func(*args, **kwargs)

        return wrapper


class Singleton:
    """单例模式"""
    @MakeSynchronized()
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)

        return cls._instance


class NoException:
    """不抛出异常"""
    def __init__(self):
        """"""

    def __call__(self, func):
        @functools.wraps(func)
        def wrappers(*args, **kwargs) -> t.Callable:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error(e)
                traceback.print_exc()

            logging.info(f'func {func.__name__} do not raise Exception')

        return wrappers
