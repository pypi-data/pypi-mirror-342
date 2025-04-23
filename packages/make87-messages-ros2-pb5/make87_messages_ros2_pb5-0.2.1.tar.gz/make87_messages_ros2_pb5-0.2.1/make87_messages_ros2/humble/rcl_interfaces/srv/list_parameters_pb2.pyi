from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rcl_interfaces.msg import list_parameters_result_pb2 as _list_parameters_result_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListParametersRequest(_message.Message):
    __slots__ = ("header", "prefixes", "depth")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PREFIXES_FIELD_NUMBER: _ClassVar[int]
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    prefixes: _containers.RepeatedScalarFieldContainer[str]
    depth: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., prefixes: _Optional[_Iterable[str]] = ..., depth: _Optional[int] = ...) -> None: ...

class ListParametersResponse(_message.Message):
    __slots__ = ("header", "result")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    result: _list_parameters_result_pb2.ListParametersResult
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., result: _Optional[_Union[_list_parameters_result_pb2.ListParametersResult, _Mapping]] = ...) -> None: ...
