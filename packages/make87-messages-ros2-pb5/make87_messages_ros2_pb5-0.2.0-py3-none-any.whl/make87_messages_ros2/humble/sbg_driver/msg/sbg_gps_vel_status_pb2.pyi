from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SbgGpsVelStatus(_message.Message):
    __slots__ = ("header", "vel_status", "vel_type")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VEL_STATUS_FIELD_NUMBER: _ClassVar[int]
    VEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    vel_status: int
    vel_type: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., vel_status: _Optional[int] = ..., vel_type: _Optional[int] = ...) -> None: ...
