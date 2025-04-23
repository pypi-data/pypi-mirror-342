from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rcl_interfaces.msg import parameter_pb2 as _parameter_pb2
from make87_messages_ros2.humble.rcl_interfaces.msg import set_parameters_result_pb2 as _set_parameters_result_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetParametersRequest(_message.Message):
    __slots__ = ("header", "parameters")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    parameters: _containers.RepeatedCompositeFieldContainer[_parameter_pb2.Parameter]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., parameters: _Optional[_Iterable[_Union[_parameter_pb2.Parameter, _Mapping]]] = ...) -> None: ...

class SetParametersResponse(_message.Message):
    __slots__ = ("header", "results")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    results: _containers.RepeatedCompositeFieldContainer[_set_parameters_result_pb2.SetParametersResult]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., results: _Optional[_Iterable[_Union[_set_parameters_result_pb2.SetParametersResult, _Mapping]]] = ...) -> None: ...
