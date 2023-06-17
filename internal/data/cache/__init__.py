import typing as t

from . import session


__all__ = [
    'CacheSession',
    'sess',
    'new_cache_session',

    'CacheType',
    'RangeIdx',
    'CacheOptions'
]


CacheSession = session.CacheSession
sess: t.Optional[CacheSession] = None
new_cache_session = session.new_cache_session

CacheType = session.CacheType
RangeIdx = session.RangeIdx
CacheOptions = session.CacheOptions
