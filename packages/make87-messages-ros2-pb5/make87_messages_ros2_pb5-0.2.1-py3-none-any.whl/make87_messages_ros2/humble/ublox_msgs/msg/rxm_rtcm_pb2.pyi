from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RxmRTCM(_message.Message):
    __slots__ = ("header", "version", "flags", "reserved0", "ref_station", "msg_type")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    REF_STATION_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    version: int
    flags: int
    reserved0: _containers.RepeatedScalarFieldContainer[int]
    ref_station: int
    msg_type: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., version: _Optional[int] = ..., flags: _Optional[int] = ..., reserved0: _Optional[_Iterable[int]] = ..., ref_station: _Optional[int] = ..., msg_type: _Optional[int] = ...) -> None: ...
