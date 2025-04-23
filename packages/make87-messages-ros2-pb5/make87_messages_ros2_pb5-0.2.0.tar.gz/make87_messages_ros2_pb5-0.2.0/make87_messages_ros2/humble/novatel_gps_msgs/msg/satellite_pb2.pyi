from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Satellite(_message.Message):
    __slots__ = ("header", "prn", "elevation", "azimuth", "snr")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PRN_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_FIELD_NUMBER: _ClassVar[int]
    AZIMUTH_FIELD_NUMBER: _ClassVar[int]
    SNR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    prn: int
    elevation: int
    azimuth: int
    snr: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., prn: _Optional[int] = ..., elevation: _Optional[int] = ..., azimuth: _Optional[int] = ..., snr: _Optional[int] = ...) -> None: ...
