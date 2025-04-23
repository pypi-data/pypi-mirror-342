from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SilhouetteMatchObject(_message.Message):
    __slots__ = ("object_id", "region_of_interest_2d_id")
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    REGION_OF_INTEREST_2D_ID_FIELD_NUMBER: _ClassVar[int]
    object_id: str
    region_of_interest_2d_id: str
    def __init__(self, object_id: _Optional[str] = ..., region_of_interest_2d_id: _Optional[str] = ...) -> None: ...
