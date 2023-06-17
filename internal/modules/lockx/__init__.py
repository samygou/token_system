import typing as t

from . import client


__all__ = [
    'Lock',
    'ILock',
    'LockPool',
]


Lock = client.Lock
ILock = client.ILock
LockPool = client.LockPool

lock_pool: t.Optional[LockPool] = None
