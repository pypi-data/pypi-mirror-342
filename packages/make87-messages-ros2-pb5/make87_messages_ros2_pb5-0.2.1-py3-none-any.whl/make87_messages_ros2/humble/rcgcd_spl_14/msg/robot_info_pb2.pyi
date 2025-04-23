from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RobotInfo(_message.Message):
    __slots__ = ("header", "penalty", "secs_till_unpenalised")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PENALTY_FIELD_NUMBER: _ClassVar[int]
    SECS_TILL_UNPENALISED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    penalty: int
    secs_till_unpenalised: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., penalty: _Optional[int] = ..., secs_till_unpenalised: _Optional[int] = ...) -> None: ...
