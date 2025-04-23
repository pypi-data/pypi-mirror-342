from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ControllerInfo(_message.Message):
    __slots__ = ("header", "type", "p_gain", "i_gain", "d_gain")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    P_GAIN_FIELD_NUMBER: _ClassVar[int]
    I_GAIN_FIELD_NUMBER: _ClassVar[int]
    D_GAIN_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    type: int
    p_gain: float
    i_gain: float
    d_gain: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., type: _Optional[int] = ..., p_gain: _Optional[float] = ..., i_gain: _Optional[float] = ..., d_gain: _Optional[float] = ...) -> None: ...
