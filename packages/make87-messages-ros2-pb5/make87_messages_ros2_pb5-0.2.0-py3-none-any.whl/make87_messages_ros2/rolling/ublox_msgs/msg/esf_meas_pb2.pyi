from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EsfMEAS(_message.Message):
    __slots__ = ("time_tag", "flags", "id", "data", "calib_t_tag")
    TIME_TAG_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    CALIB_T_TAG_FIELD_NUMBER: _ClassVar[int]
    time_tag: int
    flags: int
    id: int
    data: _containers.RepeatedScalarFieldContainer[int]
    calib_t_tag: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, time_tag: _Optional[int] = ..., flags: _Optional[int] = ..., id: _Optional[int] = ..., data: _Optional[_Iterable[int]] = ..., calib_t_tag: _Optional[_Iterable[int]] = ...) -> None: ...
