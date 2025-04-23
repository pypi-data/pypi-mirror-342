from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ur_dashboard_msgs.msg import robot_mode_pb2 as _robot_mode_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetRobotModeRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class GetRobotModeResponse(_message.Message):
    __slots__ = ("header", "robot_mode", "answer", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROBOT_MODE_FIELD_NUMBER: _ClassVar[int]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    robot_mode: _robot_mode_pb2.RobotMode
    answer: str
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., robot_mode: _Optional[_Union[_robot_mode_pb2.RobotMode, _Mapping]] = ..., answer: _Optional[str] = ..., success: bool = ...) -> None: ...
