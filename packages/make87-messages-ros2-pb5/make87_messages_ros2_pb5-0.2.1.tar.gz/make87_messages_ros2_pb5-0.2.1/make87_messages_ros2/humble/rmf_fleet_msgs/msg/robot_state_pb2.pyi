from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_fleet_msgs.msg import location_pb2 as _location_pb2
from make87_messages_ros2.humble.rmf_fleet_msgs.msg import robot_mode_pb2 as _robot_mode_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RobotState(_message.Message):
    __slots__ = ("header", "name", "model", "task_id", "seq", "mode", "battery_percent", "location", "path")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    BATTERY_PERCENT_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    model: str
    task_id: str
    seq: int
    mode: _robot_mode_pb2.RobotMode
    battery_percent: float
    location: _location_pb2.Location
    path: _containers.RepeatedCompositeFieldContainer[_location_pb2.Location]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., model: _Optional[str] = ..., task_id: _Optional[str] = ..., seq: _Optional[int] = ..., mode: _Optional[_Union[_robot_mode_pb2.RobotMode, _Mapping]] = ..., battery_percent: _Optional[float] = ..., location: _Optional[_Union[_location_pb2.Location, _Mapping]] = ..., path: _Optional[_Iterable[_Union[_location_pb2.Location, _Mapping]]] = ...) -> None: ...
