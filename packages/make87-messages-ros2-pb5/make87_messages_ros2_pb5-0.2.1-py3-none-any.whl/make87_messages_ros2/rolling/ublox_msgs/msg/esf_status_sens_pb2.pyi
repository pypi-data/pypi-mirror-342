from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EsfSTATUSSens(_message.Message):
    __slots__ = ("sens_status1", "sens_status2", "freq", "faults")
    SENS_STATUS1_FIELD_NUMBER: _ClassVar[int]
    SENS_STATUS2_FIELD_NUMBER: _ClassVar[int]
    FREQ_FIELD_NUMBER: _ClassVar[int]
    FAULTS_FIELD_NUMBER: _ClassVar[int]
    sens_status1: int
    sens_status2: int
    freq: int
    faults: int
    def __init__(self, sens_status1: _Optional[int] = ..., sens_status2: _Optional[int] = ..., freq: _Optional[int] = ..., faults: _Optional[int] = ...) -> None: ...
