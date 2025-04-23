from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.controller_manager_msgs.msg import controller_state_pb2 as _controller_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListControllersRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class ListControllersResponse(_message.Message):
    __slots__ = ("header", "controller")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONTROLLER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    controller: _containers.RepeatedCompositeFieldContainer[_controller_state_pb2.ControllerState]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., controller: _Optional[_Iterable[_Union[_controller_state_pb2.ControllerState, _Mapping]]] = ...) -> None: ...
