from make87_messages_ros2.jazzy.rcl_interfaces.msg import parameter_pb2 as _parameter_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ParamVec(_message.Message):
    __slots__ = ("header", "params")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    params: _containers.RepeatedCompositeFieldContainer[_parameter_pb2.Parameter]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., params: _Optional[_Iterable[_Union[_parameter_pb2.Parameter, _Mapping]]] = ...) -> None: ...
