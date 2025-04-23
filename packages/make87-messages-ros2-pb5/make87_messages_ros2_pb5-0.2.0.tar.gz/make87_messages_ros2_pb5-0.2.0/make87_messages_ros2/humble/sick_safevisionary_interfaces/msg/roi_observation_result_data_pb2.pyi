from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ROIObservationResultData(_message.Message):
    __slots__ = ("header", "task_result", "result_safe", "result_valid", "distance_valid", "distance_safe")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TASK_RESULT_FIELD_NUMBER: _ClassVar[int]
    RESULT_SAFE_FIELD_NUMBER: _ClassVar[int]
    RESULT_VALID_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_VALID_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_SAFE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    task_result: int
    result_safe: int
    result_valid: int
    distance_valid: int
    distance_safe: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., task_result: _Optional[int] = ..., result_safe: _Optional[int] = ..., result_valid: _Optional[int] = ..., distance_valid: _Optional[int] = ..., distance_safe: _Optional[int] = ...) -> None: ...
