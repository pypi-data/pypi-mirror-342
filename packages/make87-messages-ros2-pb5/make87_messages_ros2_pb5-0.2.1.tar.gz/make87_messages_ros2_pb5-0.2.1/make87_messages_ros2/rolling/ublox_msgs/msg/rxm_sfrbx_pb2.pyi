from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RxmSFRBX(_message.Message):
    __slots__ = ("gnss_id", "sv_id", "reserved0", "freq_id", "num_words", "chn", "version", "reserved1", "dwrd")
    GNSS_ID_FIELD_NUMBER: _ClassVar[int]
    SV_ID_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    FREQ_ID_FIELD_NUMBER: _ClassVar[int]
    NUM_WORDS_FIELD_NUMBER: _ClassVar[int]
    CHN_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    DWRD_FIELD_NUMBER: _ClassVar[int]
    gnss_id: int
    sv_id: int
    reserved0: int
    freq_id: int
    num_words: int
    chn: int
    version: int
    reserved1: int
    dwrd: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, gnss_id: _Optional[int] = ..., sv_id: _Optional[int] = ..., reserved0: _Optional[int] = ..., freq_id: _Optional[int] = ..., num_words: _Optional[int] = ..., chn: _Optional[int] = ..., version: _Optional[int] = ..., reserved1: _Optional[int] = ..., dwrd: _Optional[_Iterable[int]] = ...) -> None: ...
