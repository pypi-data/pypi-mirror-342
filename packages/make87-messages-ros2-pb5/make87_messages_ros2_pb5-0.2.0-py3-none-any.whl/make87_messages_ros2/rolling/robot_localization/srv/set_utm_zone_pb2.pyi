from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SetUTMZoneRequest(_message.Message):
    __slots__ = ("utm_zone",)
    UTM_ZONE_FIELD_NUMBER: _ClassVar[int]
    utm_zone: str
    def __init__(self, utm_zone: _Optional[str] = ...) -> None: ...

class SetUTMZoneResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
