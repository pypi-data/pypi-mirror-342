from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JointConstraint(_message.Message):
    __slots__ = ("header", "joint_name", "position", "tolerance_above", "tolerance_below", "weight")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    JOINT_NAME_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    TOLERANCE_ABOVE_FIELD_NUMBER: _ClassVar[int]
    TOLERANCE_BELOW_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    joint_name: str
    position: float
    tolerance_above: float
    tolerance_below: float
    weight: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., joint_name: _Optional[str] = ..., position: _Optional[float] = ..., tolerance_above: _Optional[float] = ..., tolerance_below: _Optional[float] = ..., weight: _Optional[float] = ...) -> None: ...
