from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

BUCKET_INCORRECTNESS: Error
CREATE_TOKEN_FAILED: Error
DESCRIPTOR: _descriptor.FileDescriptor
NOT_ENOUGH_TOKEN: Error
OK: Error
OUT_OF_RANGE_BUCKET: Error
SERVER_FAULT: Error
TOKEN_ALREADY_START: Error
TOKEN_NOT_EXIST: Error
TOKEN_NOT_START: Error
TOKEN_PER_SECOND_INCORRECTNESS: Error
TOPIC_ALREADY_EXIST: Error
TOPIC_INCORRECTNESS: Error
TOPIC_IS_NULL: Error
TOPIC_NOT_EXIST: Error

class CreateTokenReq(_message.Message):
    __slots__ = ["bucket", "tokenPerSecond", "topic"]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    TOKENPERSECOND_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    bucket: int
    tokenPerSecond: int
    topic: str
    def __init__(self, topic: _Optional[str] = ..., bucket: _Optional[int] = ..., tokenPerSecond: _Optional[int] = ...) -> None: ...

class CreateTokenResp(_message.Message):
    __slots__ = ["err"]
    ERR_FIELD_NUMBER: _ClassVar[int]
    err: Error
    def __init__(self, err: _Optional[_Union[Error, str]] = ...) -> None: ...

class DeleteTokenReq(_message.Message):
    __slots__ = ["topic"]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    topic: str
    def __init__(self, topic: _Optional[str] = ...) -> None: ...

class DeleteTokenResp(_message.Message):
    __slots__ = ["err"]
    ERR_FIELD_NUMBER: _ClassVar[int]
    err: Error
    def __init__(self, err: _Optional[_Union[Error, str]] = ...) -> None: ...

class GetTokenReq(_message.Message):
    __slots__ = ["count", "topic"]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    count: int
    topic: str
    def __init__(self, topic: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class GetTokenResp(_message.Message):
    __slots__ = ["err"]
    ERR_FIELD_NUMBER: _ClassVar[int]
    err: Error
    def __init__(self, err: _Optional[_Union[Error, str]] = ...) -> None: ...

class StartTokenReq(_message.Message):
    __slots__ = ["topic"]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    topic: str
    def __init__(self, topic: _Optional[str] = ...) -> None: ...

class StartTokenResp(_message.Message):
    __slots__ = ["err"]
    ERR_FIELD_NUMBER: _ClassVar[int]
    err: Error
    def __init__(self, err: _Optional[_Union[Error, str]] = ...) -> None: ...

class Error(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
