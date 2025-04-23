from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RxmALM(_message.Message):
    __slots__ = ("svid", "week", "dwrd")
    SVID_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    DWRD_FIELD_NUMBER: _ClassVar[int]
    svid: int
    week: int
    dwrd: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, svid: _Optional[int] = ..., week: _Optional[int] = ..., dwrd: _Optional[_Iterable[int]] = ...) -> None: ...
