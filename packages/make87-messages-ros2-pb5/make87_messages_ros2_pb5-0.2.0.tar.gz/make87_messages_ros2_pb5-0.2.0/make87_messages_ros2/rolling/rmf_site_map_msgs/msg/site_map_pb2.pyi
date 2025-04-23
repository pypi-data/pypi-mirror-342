from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SiteMap(_message.Message):
    __slots__ = ("encoding", "data")
    ENCODING_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    encoding: int
    data: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, encoding: _Optional[int] = ..., data: _Optional[_Iterable[int]] = ...) -> None: ...
