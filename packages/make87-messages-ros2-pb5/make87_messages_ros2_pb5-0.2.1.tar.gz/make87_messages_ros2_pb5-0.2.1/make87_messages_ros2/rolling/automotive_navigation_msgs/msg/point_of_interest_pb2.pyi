from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PointOfInterest(_message.Message):
    __slots__ = ("guid", "latitude", "longitude", "params")
    GUID_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    guid: int
    latitude: float
    longitude: float
    params: str
    def __init__(self, guid: _Optional[int] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., params: _Optional[str] = ...) -> None: ...
