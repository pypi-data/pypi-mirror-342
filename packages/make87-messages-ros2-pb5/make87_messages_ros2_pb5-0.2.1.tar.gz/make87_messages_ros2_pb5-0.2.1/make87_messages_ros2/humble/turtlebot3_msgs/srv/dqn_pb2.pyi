from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DqnRequest(_message.Message):
    __slots__ = ("header", "action", "init")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    INIT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    action: int
    init: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., action: _Optional[int] = ..., init: bool = ...) -> None: ...

class DqnResponse(_message.Message):
    __slots__ = ("header", "state", "reward", "done")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    REWARD_FIELD_NUMBER: _ClassVar[int]
    DONE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    state: _containers.RepeatedScalarFieldContainer[float]
    reward: float
    done: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., state: _Optional[_Iterable[float]] = ..., reward: _Optional[float] = ..., done: bool = ...) -> None: ...
