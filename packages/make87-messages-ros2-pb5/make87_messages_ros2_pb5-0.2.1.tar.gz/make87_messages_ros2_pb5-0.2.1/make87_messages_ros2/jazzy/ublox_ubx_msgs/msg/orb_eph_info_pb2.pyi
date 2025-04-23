from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class OrbEphInfo(_message.Message):
    __slots__ = ("eph_usability", "eph_source")
    EPH_USABILITY_FIELD_NUMBER: _ClassVar[int]
    EPH_SOURCE_FIELD_NUMBER: _ClassVar[int]
    eph_usability: int
    eph_source: int
    def __init__(self, eph_usability: _Optional[int] = ..., eph_source: _Optional[int] = ...) -> None: ...
