from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_task_msgs.msg import dispatch_states_pb2 as _dispatch_states_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetDispatchStatesRequest(_message.Message):
    __slots__ = ("header", "task_ids")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TASK_IDS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    task_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., task_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetDispatchStatesResponse(_message.Message):
    __slots__ = ("header", "success", "states")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    states: _dispatch_states_pb2.DispatchStates
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., states: _Optional[_Union[_dispatch_states_pb2.DispatchStates, _Mapping]] = ...) -> None: ...
