from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SilhouetteMatchObject(_message.Message):
    __slots__ = ("header", "object_id", "region_of_interest_2d_id")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    REGION_OF_INTEREST_2D_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    object_id: str
    region_of_interest_2d_id: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., object_id: _Optional[str] = ..., region_of_interest_2d_id: _Optional[str] = ...) -> None: ...
