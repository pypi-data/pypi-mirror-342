from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CfgSBAS(_message.Message):
    __slots__ = ("header", "mode", "usage", "max_sbas", "scanmode2", "scanmode1")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    MAX_SBAS_FIELD_NUMBER: _ClassVar[int]
    SCANMODE2_FIELD_NUMBER: _ClassVar[int]
    SCANMODE1_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    mode: int
    usage: int
    max_sbas: int
    scanmode2: int
    scanmode1: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., mode: _Optional[int] = ..., usage: _Optional[int] = ..., max_sbas: _Optional[int] = ..., scanmode2: _Optional[int] = ..., scanmode1: _Optional[int] = ...) -> None: ...
