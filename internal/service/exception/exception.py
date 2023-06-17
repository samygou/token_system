from functools import wraps
import typing as t
import logging
import traceback


from api.v1 import pb_token_system_pb2 as api_token_system_pb2
from internal.biz import BIZException


class APIExceptionHandler:
    """处理api exception"""
    def __init__(self, resp_func: t.Callable):
        """

        :param resp_func: 响应函数
        """
        self._resp_func = resp_func

    def __call__(self, func) -> t.Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> t.Callable:
            try:
                return func(*args, **kwargs)
            except BIZException.ErrInternalServer:
                return self._resp_func(err=api_token_system_pb2.SERVER_FAULT)
            except BIZException.ErrTopicNotExist:
                return self._resp_func(err=api_token_system_pb2.TOPIC_NOT_EXIST)
            except BIZException.ErrTopicIsNull:
                return self._resp_func(err=api_token_system_pb2.TOPIC_IS_NULL)
            except BIZException.ErrTopicAlreadyExist:
                return self._resp_func(err=api_token_system_pb2.TOPIC_ALREADY_EXIST)
            except BIZException.ErrTopicNotExactly:
                return self._resp_func(err=api_token_system_pb2.TOPIC_INCORRECTNESS)
            except BIZException.ErrTokenNotExist:
                return self._resp_func(err=api_token_system_pb2.TOPIC_NOT_EXIST)
            except BIZException.ErrTokenAlreadyStart:
                return self._resp_func(err=api_token_system_pb2.TOKEN_ALREADY_START)
            except BIZException.ErrTokenNotStart:
                return self._resp_func(err=api_token_system_pb2.TOKEN_NOT_START)
            except BIZException.ErrOutOfRangeBucket:
                return self._resp_func(err=api_token_system_pb2.OUT_OF_RANGE_BUCKET)
            except BIZException.ErrNotEnoughToken:
                return self._resp_func(err=api_token_system_pb2.NOT_ENOUGH_TOKEN)
            except BIZException.ErrBucketNotExactly:
                return self._resp_func(err=api_token_system_pb2.BUCKET_INCORRECTNESS)
            except BIZException.ErrTokenPerSecondNotExactly:
                return self._resp_func(err=api_token_system_pb2.TOKEN_PER_SECOND_INCORRECTNESS)
            except Exception as e:
                logging.error(e)
                traceback.print_exc()
                return self._resp_func(err=api_token_system_pb2.SERVER_FAULT)

        return wrapper
