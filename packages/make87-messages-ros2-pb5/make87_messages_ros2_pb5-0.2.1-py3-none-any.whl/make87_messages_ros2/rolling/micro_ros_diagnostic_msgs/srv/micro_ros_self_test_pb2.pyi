from make87_messages_ros2.rolling.micro_ros_diagnostic_msgs.msg import micro_ros_diagnostic_status_pb2 as _micro_ros_diagnostic_status_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MicroROSSelfTestRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MicroROSSelfTestResponse(_message.Message):
    __slots__ = ("id", "passed", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    PASSED_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    passed: int
    status: _micro_ros_diagnostic_status_pb2.MicroROSDiagnosticStatus
    def __init__(self, id: _Optional[str] = ..., passed: _Optional[int] = ..., status: _Optional[_Union[_micro_ros_diagnostic_status_pb2.MicroROSDiagnosticStatus, _Mapping]] = ...) -> None: ...
