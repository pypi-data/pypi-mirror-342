from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ItineraryDelay(_message.Message):
    __slots__ = ("header", "participant", "delay", "itinerary_version")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    DELAY_FIELD_NUMBER: _ClassVar[int]
    ITINERARY_VERSION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    participant: int
    delay: int
    itinerary_version: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., participant: _Optional[int] = ..., delay: _Optional[int] = ..., itinerary_version: _Optional[int] = ...) -> None: ...
