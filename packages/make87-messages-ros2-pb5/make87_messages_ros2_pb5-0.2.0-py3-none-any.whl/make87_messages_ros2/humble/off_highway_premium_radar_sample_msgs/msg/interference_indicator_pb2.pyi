from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InterferenceIndicator(_message.Message):
    __slots__ = ("header", "fov_reduction_due_to_interfence", "interference_indicator")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FOV_REDUCTION_DUE_TO_INTERFENCE_FIELD_NUMBER: _ClassVar[int]
    INTERFERENCE_INDICATOR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    fov_reduction_due_to_interfence: float
    interference_indicator: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., fov_reduction_due_to_interfence: _Optional[float] = ..., interference_indicator: _Optional[int] = ...) -> None: ...
