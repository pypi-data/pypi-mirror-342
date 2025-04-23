from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.rcl_interfaces.msg import parameter_pb2 as _parameter_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ParameterEvent(_message.Message):
    __slots__ = ("header", "stamp", "node", "new_parameters", "changed_parameters", "deleted_parameters")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    NEW_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    CHANGED_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    DELETED_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    stamp: _time_pb2.Time
    node: str
    new_parameters: _containers.RepeatedCompositeFieldContainer[_parameter_pb2.Parameter]
    changed_parameters: _containers.RepeatedCompositeFieldContainer[_parameter_pb2.Parameter]
    deleted_parameters: _containers.RepeatedCompositeFieldContainer[_parameter_pb2.Parameter]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., node: _Optional[str] = ..., new_parameters: _Optional[_Iterable[_Union[_parameter_pb2.Parameter, _Mapping]]] = ..., changed_parameters: _Optional[_Iterable[_Union[_parameter_pb2.Parameter, _Mapping]]] = ..., deleted_parameters: _Optional[_Iterable[_Union[_parameter_pb2.Parameter, _Mapping]]] = ...) -> None: ...
