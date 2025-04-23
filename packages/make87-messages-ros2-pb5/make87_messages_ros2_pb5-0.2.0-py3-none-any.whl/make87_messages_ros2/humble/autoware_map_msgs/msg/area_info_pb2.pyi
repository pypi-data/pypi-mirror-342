from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AreaInfo(_message.Message):
    __slots__ = ("header", "center_x", "center_y", "radius")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CENTER_X_FIELD_NUMBER: _ClassVar[int]
    CENTER_Y_FIELD_NUMBER: _ClassVar[int]
    RADIUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    center_x: float
    center_y: float
    radius: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., center_x: _Optional[float] = ..., center_y: _Optional[float] = ..., radius: _Optional[float] = ...) -> None: ...
