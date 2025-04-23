from make87_messages_ros2.rolling.ur_dashboard_msgs.msg import robot_mode_pb2 as _robot_mode_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetRobotModeRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetRobotModeResponse(_message.Message):
    __slots__ = ("robot_mode", "answer", "success")
    ROBOT_MODE_FIELD_NUMBER: _ClassVar[int]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    robot_mode: _robot_mode_pb2.RobotMode
    answer: str
    success: bool
    def __init__(self, robot_mode: _Optional[_Union[_robot_mode_pb2.RobotMode, _Mapping]] = ..., answer: _Optional[str] = ..., success: bool = ...) -> None: ...
