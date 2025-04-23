from make87_messages_ros2.rolling.moveit_msgs.msg import robot_state_pb2 as _robot_state_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetRobotStateFromWarehouseRequest(_message.Message):
    __slots__ = ("name", "robot")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_FIELD_NUMBER: _ClassVar[int]
    name: str
    robot: str
    def __init__(self, name: _Optional[str] = ..., robot: _Optional[str] = ...) -> None: ...

class GetRobotStateFromWarehouseResponse(_message.Message):
    __slots__ = ("state",)
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: _robot_state_pb2.RobotState
    def __init__(self, state: _Optional[_Union[_robot_state_pb2.RobotState, _Mapping]] = ...) -> None: ...
