from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CellularStatus(_message.Message):
    __slots__ = ("header", "status", "failure_reason", "type", "quality", "mcc", "mnc", "lac")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    FAILURE_REASON_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    MCC_FIELD_NUMBER: _ClassVar[int]
    MNC_FIELD_NUMBER: _ClassVar[int]
    LAC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    status: int
    failure_reason: int
    type: int
    quality: int
    mcc: int
    mnc: int
    lac: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., status: _Optional[int] = ..., failure_reason: _Optional[int] = ..., type: _Optional[int] = ..., quality: _Optional[int] = ..., mcc: _Optional[int] = ..., mnc: _Optional[int] = ..., lac: _Optional[int] = ...) -> None: ...
