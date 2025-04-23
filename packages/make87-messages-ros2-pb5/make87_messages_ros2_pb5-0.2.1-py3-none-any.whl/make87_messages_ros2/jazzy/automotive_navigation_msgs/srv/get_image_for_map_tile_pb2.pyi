from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetImageForMapTileRequest(_message.Message):
    __slots__ = ("tile_id",)
    TILE_ID_FIELD_NUMBER: _ClassVar[int]
    tile_id: str
    def __init__(self, tile_id: _Optional[str] = ...) -> None: ...

class GetImageForMapTileResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...
