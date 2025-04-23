from make87_messages_ros2.jazzy.controller_manager_msgs.msg import chain_connection_pb2 as _chain_connection_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ControllerState(_message.Message):
    __slots__ = ("name", "state", "type", "claimed_interfaces", "required_command_interfaces", "required_state_interfaces", "is_chainable", "is_chained", "exported_state_interfaces", "reference_interfaces", "chain_connections")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CLAIMED_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_COMMAND_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_STATE_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    IS_CHAINABLE_FIELD_NUMBER: _ClassVar[int]
    IS_CHAINED_FIELD_NUMBER: _ClassVar[int]
    EXPORTED_STATE_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    CHAIN_CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    name: str
    state: str
    type: str
    claimed_interfaces: _containers.RepeatedScalarFieldContainer[str]
    required_command_interfaces: _containers.RepeatedScalarFieldContainer[str]
    required_state_interfaces: _containers.RepeatedScalarFieldContainer[str]
    is_chainable: bool
    is_chained: bool
    exported_state_interfaces: _containers.RepeatedScalarFieldContainer[str]
    reference_interfaces: _containers.RepeatedScalarFieldContainer[str]
    chain_connections: _containers.RepeatedCompositeFieldContainer[_chain_connection_pb2.ChainConnection]
    def __init__(self, name: _Optional[str] = ..., state: _Optional[str] = ..., type: _Optional[str] = ..., claimed_interfaces: _Optional[_Iterable[str]] = ..., required_command_interfaces: _Optional[_Iterable[str]] = ..., required_state_interfaces: _Optional[_Iterable[str]] = ..., is_chainable: bool = ..., is_chained: bool = ..., exported_state_interfaces: _Optional[_Iterable[str]] = ..., reference_interfaces: _Optional[_Iterable[str]] = ..., chain_connections: _Optional[_Iterable[_Union[_chain_connection_pb2.ChainConnection, _Mapping]]] = ...) -> None: ...
