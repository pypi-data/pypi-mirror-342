from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SwitchControllerRequest(_message.Message):
    __slots__ = ("header", "activate_controllers", "deactivate_controllers", "start_controllers", "stop_controllers", "strictness", "start_asap", "activate_asap", "timeout")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ACTIVATE_CONTROLLERS_FIELD_NUMBER: _ClassVar[int]
    DEACTIVATE_CONTROLLERS_FIELD_NUMBER: _ClassVar[int]
    START_CONTROLLERS_FIELD_NUMBER: _ClassVar[int]
    STOP_CONTROLLERS_FIELD_NUMBER: _ClassVar[int]
    STRICTNESS_FIELD_NUMBER: _ClassVar[int]
    START_ASAP_FIELD_NUMBER: _ClassVar[int]
    ACTIVATE_ASAP_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    activate_controllers: _containers.RepeatedScalarFieldContainer[str]
    deactivate_controllers: _containers.RepeatedScalarFieldContainer[str]
    start_controllers: _containers.RepeatedScalarFieldContainer[str]
    stop_controllers: _containers.RepeatedScalarFieldContainer[str]
    strictness: int
    start_asap: bool
    activate_asap: bool
    timeout: _duration_pb2.Duration
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., activate_controllers: _Optional[_Iterable[str]] = ..., deactivate_controllers: _Optional[_Iterable[str]] = ..., start_controllers: _Optional[_Iterable[str]] = ..., stop_controllers: _Optional[_Iterable[str]] = ..., strictness: _Optional[int] = ..., start_asap: bool = ..., activate_asap: bool = ..., timeout: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class SwitchControllerResponse(_message.Message):
    __slots__ = ("header", "ok")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OK_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ok: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ok: bool = ...) -> None: ...
