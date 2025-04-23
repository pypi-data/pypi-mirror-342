from make87_messages_ros2.jazzy.plansys2_msgs.msg import param_pb2 as _param_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AffectParamRequest(_message.Message):
    __slots__ = ("param",)
    PARAM_FIELD_NUMBER: _ClassVar[int]
    param: _param_pb2.Param
    def __init__(self, param: _Optional[_Union[_param_pb2.Param, _Mapping]] = ...) -> None: ...

class AffectParamResponse(_message.Message):
    __slots__ = ("success", "error_info")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_info: str
    def __init__(self, success: bool = ..., error_info: _Optional[str] = ...) -> None: ...
