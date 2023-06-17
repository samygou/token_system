import typing as t

from . import client


__all__ = ['new_client', 'Client', 'redis', 'Lock']

new_client = client.new_client
Client = client.Client
redis: t.Optional[Client] = None
Lock = client.Lock
