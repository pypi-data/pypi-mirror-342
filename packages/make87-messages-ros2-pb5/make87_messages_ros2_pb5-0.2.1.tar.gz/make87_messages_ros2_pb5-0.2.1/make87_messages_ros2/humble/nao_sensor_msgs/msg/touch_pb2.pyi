from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Touch(_message.Message):
    __slots__ = ("header", "head_front", "head_middle", "head_rear")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    HEAD_FRONT_FIELD_NUMBER: _ClassVar[int]
    HEAD_MIDDLE_FIELD_NUMBER: _ClassVar[int]
    HEAD_REAR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    head_front: bool
    head_middle: bool
    head_rear: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., head_front: bool = ..., head_middle: bool = ..., head_rear: bool = ...) -> None: ...
