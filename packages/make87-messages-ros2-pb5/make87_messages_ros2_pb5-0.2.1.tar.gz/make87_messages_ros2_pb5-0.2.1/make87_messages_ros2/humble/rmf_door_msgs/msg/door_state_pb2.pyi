from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.rmf_door_msgs.msg import door_mode_pb2 as _door_mode_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DoorState(_message.Message):
    __slots__ = ("header", "door_time", "door_name", "current_mode")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DOOR_TIME_FIELD_NUMBER: _ClassVar[int]
    DOOR_NAME_FIELD_NUMBER: _ClassVar[int]
    CURRENT_MODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    door_time: _time_pb2.Time
    door_name: str
    current_mode: _door_mode_pb2.DoorMode
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., door_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., door_name: _Optional[str] = ..., current_mode: _Optional[_Union[_door_mode_pb2.DoorMode, _Mapping]] = ...) -> None: ...
