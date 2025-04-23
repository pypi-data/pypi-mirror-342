from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MissionUpdate(_message.Message):
    __slots__ = ("header", "drone_id", "mission_id", "item_id", "action", "mission")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DRONE_ID_FIELD_NUMBER: _ClassVar[int]
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    MISSION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    drone_id: str
    mission_id: int
    item_id: int
    action: int
    mission: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., drone_id: _Optional[str] = ..., mission_id: _Optional[int] = ..., item_id: _Optional[int] = ..., action: _Optional[int] = ..., mission: _Optional[str] = ...) -> None: ...
