from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Switches(_message.Message):
    __slots__ = ("header", "switch0", "switch1", "switch2")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SWITCH0_FIELD_NUMBER: _ClassVar[int]
    SWITCH1_FIELD_NUMBER: _ClassVar[int]
    SWITCH2_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    switch0: bool
    switch1: bool
    switch2: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., switch0: bool = ..., switch1: bool = ..., switch2: bool = ...) -> None: ...
