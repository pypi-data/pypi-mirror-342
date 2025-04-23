from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Tow(_message.Message):
    __slots__ = ("header", "task_id", "object_type", "is_object_id_known", "object_id", "pickup_place_name", "is_dropoff_place_known", "dropoff_place_name")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_OBJECT_ID_KNOWN_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PICKUP_PLACE_NAME_FIELD_NUMBER: _ClassVar[int]
    IS_DROPOFF_PLACE_KNOWN_FIELD_NUMBER: _ClassVar[int]
    DROPOFF_PLACE_NAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    task_id: str
    object_type: str
    is_object_id_known: bool
    object_id: str
    pickup_place_name: str
    is_dropoff_place_known: bool
    dropoff_place_name: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., task_id: _Optional[str] = ..., object_type: _Optional[str] = ..., is_object_id_known: bool = ..., object_id: _Optional[str] = ..., pickup_place_name: _Optional[str] = ..., is_dropoff_place_known: bool = ..., dropoff_place_name: _Optional[str] = ...) -> None: ...
