from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WheelEncoder(_message.Message):
    __slots__ = ("header", "frequency", "directional", "id")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    DIRECTIONAL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    frequency: float
    directional: bool
    id: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., frequency: _Optional[float] = ..., directional: bool = ..., id: _Optional[int] = ...) -> None: ...
