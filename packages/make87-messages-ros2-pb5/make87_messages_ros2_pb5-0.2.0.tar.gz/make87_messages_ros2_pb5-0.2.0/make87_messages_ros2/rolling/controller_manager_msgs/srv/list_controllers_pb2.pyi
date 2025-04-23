from make87_messages_ros2.rolling.controller_manager_msgs.msg import controller_state_pb2 as _controller_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListControllersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListControllersResponse(_message.Message):
    __slots__ = ("controller",)
    CONTROLLER_FIELD_NUMBER: _ClassVar[int]
    controller: _containers.RepeatedCompositeFieldContainer[_controller_state_pb2.ControllerState]
    def __init__(self, controller: _Optional[_Iterable[_Union[_controller_state_pb2.ControllerState, _Mapping]]] = ...) -> None: ...
