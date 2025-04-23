from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.adi_tmcl.msg import tmc_param_pb2 as _tmc_param_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TmcGgpAllRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class TmcGgpAllResponse(_message.Message):
    __slots__ = ("header", "success", "param")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    PARAM_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    param: _containers.RepeatedCompositeFieldContainer[_tmc_param_pb2.TmcParam]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., param: _Optional[_Iterable[_Union[_tmc_param_pb2.TmcParam, _Mapping]]] = ...) -> None: ...
