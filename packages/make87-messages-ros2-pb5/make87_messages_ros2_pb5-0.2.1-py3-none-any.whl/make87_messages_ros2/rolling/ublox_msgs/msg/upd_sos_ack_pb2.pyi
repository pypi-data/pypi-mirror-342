from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UpdSOSAck(_message.Message):
    __slots__ = ("cmd", "reserved0", "response", "reserved1")
    CMD_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    cmd: int
    reserved0: _containers.RepeatedScalarFieldContainer[int]
    response: int
    reserved1: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, cmd: _Optional[int] = ..., reserved0: _Optional[_Iterable[int]] = ..., response: _Optional[int] = ..., reserved1: _Optional[_Iterable[int]] = ...) -> None: ...
