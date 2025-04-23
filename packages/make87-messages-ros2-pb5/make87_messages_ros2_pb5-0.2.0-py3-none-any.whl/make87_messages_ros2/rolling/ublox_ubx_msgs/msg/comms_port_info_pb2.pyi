from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CommsPortInfo(_message.Message):
    __slots__ = ("port_id", "tx_pending", "tx_bytes", "tx_usage", "tx_peak_usage", "rx_pending", "rx_bytes", "rx_usage", "rx_peak_usage", "overrun_errs", "msgs", "skipped")
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    TX_PENDING_FIELD_NUMBER: _ClassVar[int]
    TX_BYTES_FIELD_NUMBER: _ClassVar[int]
    TX_USAGE_FIELD_NUMBER: _ClassVar[int]
    TX_PEAK_USAGE_FIELD_NUMBER: _ClassVar[int]
    RX_PENDING_FIELD_NUMBER: _ClassVar[int]
    RX_BYTES_FIELD_NUMBER: _ClassVar[int]
    RX_USAGE_FIELD_NUMBER: _ClassVar[int]
    RX_PEAK_USAGE_FIELD_NUMBER: _ClassVar[int]
    OVERRUN_ERRS_FIELD_NUMBER: _ClassVar[int]
    MSGS_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_FIELD_NUMBER: _ClassVar[int]
    port_id: int
    tx_pending: int
    tx_bytes: int
    tx_usage: int
    tx_peak_usage: int
    rx_pending: int
    rx_bytes: int
    rx_usage: int
    rx_peak_usage: int
    overrun_errs: int
    msgs: _containers.RepeatedScalarFieldContainer[int]
    skipped: int
    def __init__(self, port_id: _Optional[int] = ..., tx_pending: _Optional[int] = ..., tx_bytes: _Optional[int] = ..., tx_usage: _Optional[int] = ..., tx_peak_usage: _Optional[int] = ..., rx_pending: _Optional[int] = ..., rx_bytes: _Optional[int] = ..., rx_usage: _Optional[int] = ..., rx_peak_usage: _Optional[int] = ..., overrun_errs: _Optional[int] = ..., msgs: _Optional[_Iterable[int]] = ..., skipped: _Optional[int] = ...) -> None: ...
