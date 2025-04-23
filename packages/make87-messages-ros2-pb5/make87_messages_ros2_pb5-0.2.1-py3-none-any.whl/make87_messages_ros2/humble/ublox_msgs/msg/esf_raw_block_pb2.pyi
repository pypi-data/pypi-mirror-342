from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsfRAWBlock(_message.Message):
    __slots__ = ("header", "data", "s_t_tag")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    S_T_TAG_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    data: int
    s_t_tag: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., data: _Optional[int] = ..., s_t_tag: _Optional[int] = ...) -> None: ...
