from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CfgGNSSBlock(_message.Message):
    __slots__ = ("header", "gnss_id", "res_trk_ch", "max_trk_ch", "reserved1", "flags")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GNSS_ID_FIELD_NUMBER: _ClassVar[int]
    RES_TRK_CH_FIELD_NUMBER: _ClassVar[int]
    MAX_TRK_CH_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    gnss_id: int
    res_trk_ch: int
    max_trk_ch: int
    reserved1: int
    flags: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., gnss_id: _Optional[int] = ..., res_trk_ch: _Optional[int] = ..., max_trk_ch: _Optional[int] = ..., reserved1: _Optional[int] = ..., flags: _Optional[int] = ...) -> None: ...
