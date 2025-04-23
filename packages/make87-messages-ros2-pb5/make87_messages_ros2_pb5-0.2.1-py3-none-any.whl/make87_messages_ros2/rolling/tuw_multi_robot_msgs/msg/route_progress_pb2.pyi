from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RouteProgress(_message.Message):
    __slots__ = ("header", "passed", "current", "todo", "progress")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PASSED_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    TODO_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    passed: _containers.RepeatedScalarFieldContainer[int]
    current: int
    todo: _containers.RepeatedScalarFieldContainer[int]
    progress: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., passed: _Optional[_Iterable[int]] = ..., current: _Optional[int] = ..., todo: _Optional[_Iterable[int]] = ..., progress: _Optional[float] = ...) -> None: ...
