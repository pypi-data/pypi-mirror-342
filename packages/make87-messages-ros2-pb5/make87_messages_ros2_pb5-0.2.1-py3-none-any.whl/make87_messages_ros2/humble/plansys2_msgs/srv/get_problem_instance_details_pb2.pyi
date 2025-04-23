from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.plansys2_msgs.msg import param_pb2 as _param_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetProblemInstanceDetailsRequest(_message.Message):
    __slots__ = ("header", "instance")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    instance: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., instance: _Optional[str] = ...) -> None: ...

class GetProblemInstanceDetailsResponse(_message.Message):
    __slots__ = ("header", "success", "instance", "error_info")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    instance: _param_pb2.Param
    error_info: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., instance: _Optional[_Union[_param_pb2.Param, _Mapping]] = ..., error_info: _Optional[str] = ...) -> None: ...
