from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BlockadeCancel(_message.Message):
    __slots__ = ("header", "participant", "all_reservations", "reservation")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    ALL_RESERVATIONS_FIELD_NUMBER: _ClassVar[int]
    RESERVATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    participant: int
    all_reservations: bool
    reservation: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., participant: _Optional[int] = ..., all_reservations: bool = ..., reservation: _Optional[int] = ...) -> None: ...
