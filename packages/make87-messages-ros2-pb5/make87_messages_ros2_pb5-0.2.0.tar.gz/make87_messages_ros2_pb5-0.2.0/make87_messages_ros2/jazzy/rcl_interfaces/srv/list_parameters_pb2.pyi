from make87_messages_ros2.jazzy.rcl_interfaces.msg import list_parameters_result_pb2 as _list_parameters_result_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListParametersRequest(_message.Message):
    __slots__ = ("prefixes", "depth")
    PREFIXES_FIELD_NUMBER: _ClassVar[int]
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    prefixes: _containers.RepeatedScalarFieldContainer[str]
    depth: int
    def __init__(self, prefixes: _Optional[_Iterable[str]] = ..., depth: _Optional[int] = ...) -> None: ...

class ListParametersResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: _list_parameters_result_pb2.ListParametersResult
    def __init__(self, result: _Optional[_Union[_list_parameters_result_pb2.ListParametersResult, _Mapping]] = ...) -> None: ...
