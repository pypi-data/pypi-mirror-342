from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Robot(_message.Message):
    __slots__ = ("header", "player_number", "team", "state", "facing")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PLAYER_NUMBER_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    FACING_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    player_number: int
    team: int
    state: int
    facing: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., player_number: _Optional[int] = ..., team: _Optional[int] = ..., state: _Optional[int] = ..., facing: _Optional[int] = ...) -> None: ...
