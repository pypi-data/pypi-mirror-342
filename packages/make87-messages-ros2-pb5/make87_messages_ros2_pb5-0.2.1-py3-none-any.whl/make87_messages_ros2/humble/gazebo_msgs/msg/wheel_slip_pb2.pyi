from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WheelSlip(_message.Message):
    __slots__ = ("header", "name", "lateral_slip", "longitudinal_slip")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LATERAL_SLIP_FIELD_NUMBER: _ClassVar[int]
    LONGITUDINAL_SLIP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: _containers.RepeatedScalarFieldContainer[str]
    lateral_slip: _containers.RepeatedScalarFieldContainer[float]
    longitudinal_slip: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[_Iterable[str]] = ..., lateral_slip: _Optional[_Iterable[float]] = ..., longitudinal_slip: _Optional[_Iterable[float]] = ...) -> None: ...
