from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JamStateCentFreq(_message.Message):
    __slots__ = ("header", "cent_freq", "jammed")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CENT_FREQ_FIELD_NUMBER: _ClassVar[int]
    JAMMED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    cent_freq: int
    jammed: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., cent_freq: _Optional[int] = ..., jammed: bool = ...) -> None: ...
