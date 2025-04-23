from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Connection(_message.Message):
    __slots__ = ("header", "bitrate", "txpower", "link_quality_raw", "link_quality", "signal_level", "noise_level", "essid", "bssid", "frequency")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BITRATE_FIELD_NUMBER: _ClassVar[int]
    TXPOWER_FIELD_NUMBER: _ClassVar[int]
    LINK_QUALITY_RAW_FIELD_NUMBER: _ClassVar[int]
    LINK_QUALITY_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_LEVEL_FIELD_NUMBER: _ClassVar[int]
    NOISE_LEVEL_FIELD_NUMBER: _ClassVar[int]
    ESSID_FIELD_NUMBER: _ClassVar[int]
    BSSID_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    bitrate: float
    txpower: int
    link_quality_raw: str
    link_quality: float
    signal_level: int
    noise_level: int
    essid: str
    bssid: str
    frequency: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., bitrate: _Optional[float] = ..., txpower: _Optional[int] = ..., link_quality_raw: _Optional[str] = ..., link_quality: _Optional[float] = ..., signal_level: _Optional[int] = ..., noise_level: _Optional[int] = ..., essid: _Optional[str] = ..., bssid: _Optional[str] = ..., frequency: _Optional[float] = ...) -> None: ...
