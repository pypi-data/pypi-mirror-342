from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RadioStatus(_message.Message):
    __slots__ = ("header", "rssi", "remrssi", "txbuf", "noise", "remnoise", "rxerrors", "fixed", "rssi_dbm", "remrssi_dbm")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RSSI_FIELD_NUMBER: _ClassVar[int]
    REMRSSI_FIELD_NUMBER: _ClassVar[int]
    TXBUF_FIELD_NUMBER: _ClassVar[int]
    NOISE_FIELD_NUMBER: _ClassVar[int]
    REMNOISE_FIELD_NUMBER: _ClassVar[int]
    RXERRORS_FIELD_NUMBER: _ClassVar[int]
    FIXED_FIELD_NUMBER: _ClassVar[int]
    RSSI_DBM_FIELD_NUMBER: _ClassVar[int]
    REMRSSI_DBM_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    rssi: int
    remrssi: int
    txbuf: int
    noise: int
    remnoise: int
    rxerrors: int
    fixed: int
    rssi_dbm: float
    remrssi_dbm: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., rssi: _Optional[int] = ..., remrssi: _Optional[int] = ..., txbuf: _Optional[int] = ..., noise: _Optional[int] = ..., remnoise: _Optional[int] = ..., rxerrors: _Optional[int] = ..., fixed: _Optional[int] = ..., rssi_dbm: _Optional[float] = ..., remrssi_dbm: _Optional[float] = ...) -> None: ...
