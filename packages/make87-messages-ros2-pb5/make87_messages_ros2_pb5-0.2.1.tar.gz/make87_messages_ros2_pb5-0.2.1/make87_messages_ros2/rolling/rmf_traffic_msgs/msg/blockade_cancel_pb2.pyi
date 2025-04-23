from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BlockadeCancel(_message.Message):
    __slots__ = ("participant", "all_reservations", "reservation")
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    ALL_RESERVATIONS_FIELD_NUMBER: _ClassVar[int]
    RESERVATION_FIELD_NUMBER: _ClassVar[int]
    participant: int
    all_reservations: bool
    reservation: int
    def __init__(self, participant: _Optional[int] = ..., all_reservations: bool = ..., reservation: _Optional[int] = ...) -> None: ...
