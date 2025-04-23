from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rcss3d_agent_msgs.msg import ball_pb2 as _ball_pb2
from make87_messages_ros2.humble.rcss3d_agent_msgs.msg import field_line_pb2 as _field_line_pb2
from make87_messages_ros2.humble.rcss3d_agent_msgs.msg import flag_pb2 as _flag_pb2
from make87_messages_ros2.humble.rcss3d_agent_msgs.msg import goalpost_pb2 as _goalpost_pb2
from make87_messages_ros2.humble.rcss3d_agent_msgs.msg import player_pb2 as _player_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Vision(_message.Message):
    __slots__ = ("header", "ball", "field_lines", "flags", "goalposts", "players")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BALL_FIELD_NUMBER: _ClassVar[int]
    FIELD_LINES_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    GOALPOSTS_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ball: _containers.RepeatedCompositeFieldContainer[_ball_pb2.Ball]
    field_lines: _containers.RepeatedCompositeFieldContainer[_field_line_pb2.FieldLine]
    flags: _containers.RepeatedCompositeFieldContainer[_flag_pb2.Flag]
    goalposts: _containers.RepeatedCompositeFieldContainer[_goalpost_pb2.Goalpost]
    players: _containers.RepeatedCompositeFieldContainer[_player_pb2.Player]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ball: _Optional[_Iterable[_Union[_ball_pb2.Ball, _Mapping]]] = ..., field_lines: _Optional[_Iterable[_Union[_field_line_pb2.FieldLine, _Mapping]]] = ..., flags: _Optional[_Iterable[_Union[_flag_pb2.Flag, _Mapping]]] = ..., goalposts: _Optional[_Iterable[_Union[_goalpost_pb2.Goalpost, _Mapping]]] = ..., players: _Optional[_Iterable[_Union[_player_pb2.Player, _Mapping]]] = ...) -> None: ...
