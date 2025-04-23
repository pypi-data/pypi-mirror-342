from make87_messages_ros2.jazzy.controller_manager_msgs.msg import hardware_interface_pb2 as _hardware_interface_pb2
from make87_messages_ros2.jazzy.lifecycle_msgs.msg import state_pb2 as _state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HardwareComponentState(_message.Message):
    __slots__ = ("name", "type", "class_type", "plugin_name", "state", "command_interfaces", "state_interfaces")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CLASS_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLUGIN_NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    COMMAND_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    STATE_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: str
    class_type: str
    plugin_name: str
    state: _state_pb2.State
    command_interfaces: _containers.RepeatedCompositeFieldContainer[_hardware_interface_pb2.HardwareInterface]
    state_interfaces: _containers.RepeatedCompositeFieldContainer[_hardware_interface_pb2.HardwareInterface]
    def __init__(self, name: _Optional[str] = ..., type: _Optional[str] = ..., class_type: _Optional[str] = ..., plugin_name: _Optional[str] = ..., state: _Optional[_Union[_state_pb2.State, _Mapping]] = ..., command_interfaces: _Optional[_Iterable[_Union[_hardware_interface_pb2.HardwareInterface, _Mapping]]] = ..., state_interfaces: _Optional[_Iterable[_Union[_hardware_interface_pb2.HardwareInterface, _Mapping]]] = ...) -> None: ...
