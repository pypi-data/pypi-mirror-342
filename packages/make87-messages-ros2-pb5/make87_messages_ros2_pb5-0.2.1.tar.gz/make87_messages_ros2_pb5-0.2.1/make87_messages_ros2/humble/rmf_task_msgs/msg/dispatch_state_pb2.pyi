from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_task_msgs.msg import assignment_pb2 as _assignment_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DispatchState(_message.Message):
    __slots__ = ("header", "task_id", "status", "assignment", "errors")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNMENT_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    task_id: str
    status: int
    assignment: _assignment_pb2.Assignment
    errors: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., task_id: _Optional[str] = ..., status: _Optional[int] = ..., assignment: _Optional[_Union[_assignment_pb2.Assignment, _Mapping]] = ..., errors: _Optional[_Iterable[str]] = ...) -> None: ...
