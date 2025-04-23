from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsfSTATUSSens(_message.Message):
    __slots__ = ("header", "sens_status1", "sens_status2", "freq", "faults")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SENS_STATUS1_FIELD_NUMBER: _ClassVar[int]
    SENS_STATUS2_FIELD_NUMBER: _ClassVar[int]
    FREQ_FIELD_NUMBER: _ClassVar[int]
    FAULTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sens_status1: int
    sens_status2: int
    freq: int
    faults: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sens_status1: _Optional[int] = ..., sens_status2: _Optional[int] = ..., freq: _Optional[int] = ..., faults: _Optional[int] = ...) -> None: ...
