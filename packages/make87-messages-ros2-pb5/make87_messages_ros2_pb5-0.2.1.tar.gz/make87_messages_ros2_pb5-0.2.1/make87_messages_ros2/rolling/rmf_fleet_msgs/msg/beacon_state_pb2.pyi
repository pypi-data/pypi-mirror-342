from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BeaconState(_message.Message):
    __slots__ = ("id", "online", "category", "activated", "level")
    ID_FIELD_NUMBER: _ClassVar[int]
    ONLINE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    ACTIVATED_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    id: str
    online: bool
    category: str
    activated: bool
    level: str
    def __init__(self, id: _Optional[str] = ..., online: bool = ..., category: _Optional[str] = ..., activated: bool = ..., level: _Optional[str] = ...) -> None: ...
