from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ur_dashboard_msgs.msg import safety_mode_pb2 as _safety_mode_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetSafetyModeRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class GetSafetyModeResponse(_message.Message):
    __slots__ = ("header", "safety_mode", "answer", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SAFETY_MODE_FIELD_NUMBER: _ClassVar[int]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    safety_mode: _safety_mode_pb2.SafetyMode
    answer: str
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., safety_mode: _Optional[_Union[_safety_mode_pb2.SafetyMode, _Mapping]] = ..., answer: _Optional[str] = ..., success: bool = ...) -> None: ...
