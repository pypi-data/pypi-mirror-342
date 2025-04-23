from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.controller_manager_msgs.msg import hardware_component_state_pb2 as _hardware_component_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListHardwareComponentsRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class ListHardwareComponentsResponse(_message.Message):
    __slots__ = ("header", "component")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    component: _containers.RepeatedCompositeFieldContainer[_hardware_component_state_pb2.HardwareComponentState]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., component: _Optional[_Iterable[_Union[_hardware_component_state_pb2.HardwareComponentState, _Mapping]]] = ...) -> None: ...
