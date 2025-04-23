from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.diagnostic_msgs.msg import diagnostic_status_pb2 as _diagnostic_status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SelfTestRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class SelfTestResponse(_message.Message):
    __slots__ = ("header", "id", "passed", "status")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PASSED_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: str
    passed: int
    status: _containers.RepeatedCompositeFieldContainer[_diagnostic_status_pb2.DiagnosticStatus]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[str] = ..., passed: _Optional[int] = ..., status: _Optional[_Iterable[_Union[_diagnostic_status_pb2.DiagnosticStatus, _Mapping]]] = ...) -> None: ...
