from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.lifecycle_msgs.msg import state_pb2 as _state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetAvailableStatesRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class GetAvailableStatesResponse(_message.Message):
    __slots__ = ("header", "available_states")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_STATES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    available_states: _containers.RepeatedCompositeFieldContainer[_state_pb2.State]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., available_states: _Optional[_Iterable[_Union[_state_pb2.State, _Mapping]]] = ...) -> None: ...
