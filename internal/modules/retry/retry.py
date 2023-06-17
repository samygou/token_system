from functools import wraps
import typing as t
import traceback
import logging
import time


class Retry:
    """处理api exception"""

    def __init__(self, times: int = 1):
        """
        默认不重试
        :param times: retry times
        """
        self._times = times

    def __call__(self, func) -> t.Callable:
        @wraps(func)
        def wrappers(*args, **kwargs) -> t.Callable:
            count = 0
            while count < self._times:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.error(e)
                    traceback.print_exc()

                count += 1
                time.sleep(0.0001)   # 做短时间的休眠再重试

                logging.info(f'func {func.__name__} retry times: {count}')

        return wrappers
