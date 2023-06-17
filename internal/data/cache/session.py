import contextlib
import time
import typing as t
import json
import uuid
import copy
import logging
from enum import Enum, unique

from pydantic import BaseModel

from internal.modules import redisx
# from internal.modules import pagex
from internal.modules import retry
from internal.modules import lockx


@unique
class CacheType(Enum):
    """"""
    STRING = 1
    LIST = 2
    HASH = 3
    ZSET = 4


class RangeIdx(BaseModel):
    start: int = 0
    end: int = -1


class CacheOptions(BaseModel):
    """cache type options"""
    cacheType: CacheType = CacheType.STRING
    rangeIdx: t.Optional[RangeIdx] = None
    hashFields: t.Optional[t.List[str]] = None


class CacheSession:
    """cache session"""
    def __init__(self, session: redisx.Client):
        self._sess = session

    @contextlib.contextmanager
    def context(self):
        yield self

    # @staticmethod
    # def process_db_page_limit(pl: pagex.Pagex) -> pagex.Pagex:
    #     """
    #     从db中获取数据的偏移量处理
    #     :param pl:
    #     :return:
    #     """
    #     if pl.offset + pl.size <= 10000:
    #         db_pl = pagex.Pagex(offset=0, size=10000)
    #     else:
    #         db_pl = pl
    #
    #     return db_pl

    @retry.Retry(times=5)
    def exist_cache(
            self,
            cache_name: t.Union[t.List[str], str]
    ) -> bool:
        """
        判断缓存是否存在
        :param cache_name:
        :return:
        """
        if isinstance(cache_name, str):
            cache_name = [cache_name]
        exists = self._sess.cli.exists(*cache_name)

        return exists != 0

    @retry.Retry(times=5)
    def _list_cache_get(self, cache_name: str, start: int, end: int) -> t.List[t.Any]:
        cache_data = self._sess.cli.lrange(cache_name, start, end)
        cache_data = list(map(lambda record: json.loads(record), cache_data))
        cache_data = [] if len(cache_data) == 1 and not cache_data[0] else cache_data

        return cache_data

    @retry.Retry(times=5)
    def _list_cache_set(self, cache_name: str, cache_data: t.List[str], expired: int):
        """
        list cache set
        :param cache_name:
        :param cache_data:
        :param expired:
        :return:
        """
        self._sess.cli.delete(cache_name)
        cache_data = cache_data if cache_data else [None]
        cache_data = list(map(json.dumps, cache_data))
        self._sess.cli.rpush(cache_name, *cache_data)
        self._sess.cli.expire(cache_name, expired)

    @retry.Retry(times=5)
    def _hash_cache_get(self, cache_name: str, fields: t.List[str]) -> t.Dict[str, t.Any]:
        """

        :param cache_name:
        :param fields:
        :return:
        """
        cache_data = self._sess.cli.hmget(cache_name, fields)
        cache_data = list(map(json.loads, cache_data))
        cache_data = dict(zip(fields, cache_data))

        return cache_data

    @retry.Retry(times=5)
    def _hash_cache_set(self, cache_name: str, cache_data: t.Dict[str, str], expired: int):
        """"""
        if not isinstance(cache_data, t.Dict):
            return
        self._sess.cli.hmset(cache_name, cache_data)

        fields = [key for key in cache_data]
        self._hash_cache_expired_set(cache_name, fields, expired)

    @retry.Retry(times=5)
    def _hash_cache_expired_set(self, cache_name: str, fields: t.List[str], expired: int):
        """
        设置hash类型的fields的过期时间
        :param cache_name:
        :param fields:
        :param expired:
        :return:
        """
        for field in fields:
            cache_expired_key = f'{cache_name}-{field}-expired-key'
            val = str(uuid.uuid4())
            self._sess.cli.set(cache_expired_key, val, nx=True, ex=expired)

    @retry.Retry(times=5)
    def _hash_cache_expired_check(self, cache_name: str, fields: t.List[str]) -> (t.List[str], t.List[str]):
        """
        检查过期时间
        :param cache_name:
        :param fields:
        :return: (过期field, 有效field)
        """
        expired_fields = []
        effective_fields = []
        for field in fields:
            cache_expired_key = f'{cache_name}-{field}-expired-key'
            if not self.exist_cache(cache_expired_key):
                expired_fields.append(field)
            else:
                effective_fields.append(field)

        return expired_fields, effective_fields

    @retry.Retry(times=5)
    def _hash_fields_delete(self, cache_name: str, expired_fields: t.List[str]):
        """

        :param cache_name:
        :param expired_fields:
        :return:
        """
        self._sess.cli.hdel(cache_name, expired_fields)

    @retry.Retry(times=5)
    def _zset_cache_get(self, cache_name: str, start: int, end: int) -> t.List[t.Any]:
        """

        :param cache_name:
        :param start:
        :param end:
        :return:
        """
        cache_data = self._sess.cli.zrange(cache_name, start, end)
        cache_data = list(map(lambda record: json.loads(record), cache_data))
        cache_data = [] if len(cache_data) == 1 and not cache_data[0] else cache_data

        return cache_data

    @retry.Retry(times=5)
    def _zset_cache_set(self, cache_name: str, cache_data: t.Dict[str, float], expired: int):
        """"""
        self._sess.cli.delete(cache_name)
        if not isinstance(cache_data, dict):
            return
        self._sess.cli.zadd(cache_name, cache_data)
        self._sess.cli.expired(cache_name, expired)

    @retry.Retry(times=5)
    def _str_cache_get(self, cache_name: str, start: int, end: int) -> t.Any:
        cache_data = self._sess.cli.get(cache_name)
        cache_data = json.loads(cache_data)
        cache_data = cache_data[start:end]

        return cache_data

    @retry.Retry(times=5)
    def _str_cache_set(self, cache_name: str, cache_data: t.Union[str, list, dict], expired: int):
        if not isinstance(cache_data, str):
            cache_data = json.dumps(cache_data)
        self._sess.cli.set(cache_name, cache_data, ex=expired)

    @retry.Retry(times=5)
    def cache_delete(self, cache_name: str):
        """

        :param cache_name:
        :return:
        """
        self._sess.cli.delete(cache_name)

    # def cache(
    #         self,
    #         cache_name: str,
    #         cacheOpts: CacheOptions,
    #         cacheExpired: int,
    #         cacheWaitTimeout: int,
    #         lockExpired: int,
    #         req: t.Any,
    #         get_cache_from_db_func: t.Callable,
    # ):
    #     """
    #     缓存
    #     :param cache_name:
    #     :param cacheOpts:
    #     :param cacheExpired:
    #     :param cacheWaitTimeout:
    #     :param lockExpired:
    #     :param req:
    #     :param get_cache_from_db_func:
    #     :return:
    #     """
    #     timeout = int(time.time()) + cacheWaitTimeout
    #
    #     lock_name = f'{cache_name}-nx-lock'
    #
    #     while int(time.time()) < timeout:
    #         # 1. exist cache
    #         if self.exist_cache(cache_name):
    #             logging.info('get data from cache')
    #
    #             # 2. get data from cache
    #             # cache_data = self.get_cache(cache_name, cacheOpts)
    #             if cacheOpts.cacheType == CacheType.LIST:
    #                 cache_data = self._list_cache_get(cache_name, cacheOpts.rangeIdx.start, cacheOpts.rangeIdx.end)
    #             elif cacheOpts.cacheType == CacheType.HASH:
    #                 # 1). check expired
    #                 expired_fields, effective_fields = self._hash_cache_expired_check(cache_name, cacheOpts.hashFields)
    #                 # 2). 获取数据
    #                 cache_data = self._hash_cache_get(cache_name, effective_fields)
    #                 if expired_fields:
    #                     # 3). 删除过期的
    #                     self._hash_fields_delete(cache_name, expired_fields)
    #                     # 4). 从db中获取过期的fields
    #                     expired_data = get_cache_from_db_func(req, expired_fields)
    #                     # 5). update cache_data
    #                     cache_data.update(expired_data)
    #                     # 6). 重新设置cache中的过期fields
    #                     expired_data = {k: json.dumps(v) for k, v in zip(expired_data.keys(), expired_data.values())}
    #                     self._hash_cache_set(cache_name, expired_data, cacheExpired)
    #             elif cacheOpts.cacheType == CacheType.ZSET:
    #                 cache_data = self._zset_cache_get(cache_name, cacheOpts.rangeIdx.start, cacheOpts.rangeIdx.end)
    #             else:
    #                 cache_data = self._str_cache_get(cache_name, cacheOpts.rangeIdx.start, cacheOpts.rangeIdx.end)
    #
    #             return cache_data
    #         else:
    #             lock = lockx.Lock(lock_name, lockExpired, lockx.LockCli.ETCD)
    #             if lock.acquire():
    #                 logging.info('acquire lock, get data from db')
    #                 origin_req = copy.deepcopy(req)
    #                 # 从数据库中获取默认获取前1w条数据
    #                 req.pl = self.process_db_page_limit(req.pl)
    #                 data = get_cache_from_db_func(req)
    #                 cache_expired = cacheExpired if data else 5 * 60
    #
    #                 # 4. 更新缓存
    #                 logging.info('update cache...')
    #                 if cacheOpts.cacheType == CacheType.LIST:
    #                     self._list_cache_set(cache_name, data, cache_expired)
    #                 elif cacheOpts.cacheType == CacheType.HASH:
    #                     self._hash_cache_set(cache_name, data, cache_expired)
    #                 elif cacheOpts.cacheType == CacheType.ZSET:
    #                     self._zset_cache_set(cache_name, data, cache_expired)
    #                 else:
    #                     self._str_cache_set(cache_name, data, cache_expired)
    #                 logging.info('cache update success')
    #
    #                 # 睡眠1毫秒, 防止删除锁的一瞬间, 刚好有请求判断锁不存在, 重新更新缓存
    #                 time.sleep(0.0001)
    #
    #                 # 5. 删除锁
    #                 lock.release()
    #
    #                 return data[origin_req.pl.offset:origin_req.pl.offset + origin_req.pl.size]
    #
    #         time.sleep(0.0001)
    #         logging.info('wait cache update...')
    #
    #     return None


def new_cache_session(session: redisx.Client) -> CacheSession:
    return CacheSession(session)
