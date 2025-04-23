from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResolutionInfo(_message.Message):
    __slots__ = ("header", "resolution_start_angle", "resolution")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_START_ANGLE_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    resolution_start_angle: float
    resolution: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., resolution_start_angle: _Optional[float] = ..., resolution: _Optional[float] = ...) -> None: ...
