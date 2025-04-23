from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NavDGPSSV(_message.Message):
    __slots__ = ("header", "svid", "flags", "age_c", "prc", "prrc")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SVID_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    AGE_C_FIELD_NUMBER: _ClassVar[int]
    PRC_FIELD_NUMBER: _ClassVar[int]
    PRRC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    svid: int
    flags: int
    age_c: int
    prc: float
    prrc: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., svid: _Optional[int] = ..., flags: _Optional[int] = ..., age_c: _Optional[int] = ..., prc: _Optional[float] = ..., prrc: _Optional[float] = ...) -> None: ...
