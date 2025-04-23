from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsfMEAS(_message.Message):
    __slots__ = ("header", "time_tag", "flags", "id", "data", "calib_t_tag")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_TAG_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    CALIB_T_TAG_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    time_tag: int
    flags: int
    id: int
    data: _containers.RepeatedScalarFieldContainer[int]
    calib_t_tag: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., time_tag: _Optional[int] = ..., flags: _Optional[int] = ..., id: _Optional[int] = ..., data: _Optional[_Iterable[int]] = ..., calib_t_tag: _Optional[_Iterable[int]] = ...) -> None: ...
