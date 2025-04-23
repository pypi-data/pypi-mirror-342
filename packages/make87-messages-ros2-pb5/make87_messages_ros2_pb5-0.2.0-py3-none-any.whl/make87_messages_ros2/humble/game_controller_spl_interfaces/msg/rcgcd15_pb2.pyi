from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.game_controller_spl_interfaces.msg import team_info15_pb2 as _team_info15_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RCGCD15(_message.Message):
    __slots__ = ("header", "packet_number", "players_per_team", "competition_phase", "competition_type", "game_phase", "state", "set_play", "first_half", "kicking_team", "secs_remaining", "secondary_time", "teams")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PACKET_NUMBER_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_PER_TEAM_FIELD_NUMBER: _ClassVar[int]
    COMPETITION_PHASE_FIELD_NUMBER: _ClassVar[int]
    COMPETITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    GAME_PHASE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    SET_PLAY_FIELD_NUMBER: _ClassVar[int]
    FIRST_HALF_FIELD_NUMBER: _ClassVar[int]
    KICKING_TEAM_FIELD_NUMBER: _ClassVar[int]
    SECS_REMAINING_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_TIME_FIELD_NUMBER: _ClassVar[int]
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    packet_number: int
    players_per_team: int
    competition_phase: int
    competition_type: int
    game_phase: int
    state: int
    set_play: int
    first_half: int
    kicking_team: int
    secs_remaining: int
    secondary_time: int
    teams: _containers.RepeatedCompositeFieldContainer[_team_info15_pb2.TeamInfo15]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., packet_number: _Optional[int] = ..., players_per_team: _Optional[int] = ..., competition_phase: _Optional[int] = ..., competition_type: _Optional[int] = ..., game_phase: _Optional[int] = ..., state: _Optional[int] = ..., set_play: _Optional[int] = ..., first_half: _Optional[int] = ..., kicking_team: _Optional[int] = ..., secs_remaining: _Optional[int] = ..., secondary_time: _Optional[int] = ..., teams: _Optional[_Iterable[_Union[_team_info15_pb2.TeamInfo15, _Mapping]]] = ...) -> None: ...
