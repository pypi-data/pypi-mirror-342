from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MeasxData(_message.Message):
    __slots__ = ("header", "gnss_id", "sv_id", "c_no", "mpath_indic", "doppler_ms", "doppler_hz", "whole_chips", "frac_chips", "code_phase", "int_code_phase", "pseu_range_rms_err")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GNSS_ID_FIELD_NUMBER: _ClassVar[int]
    SV_ID_FIELD_NUMBER: _ClassVar[int]
    C_NO_FIELD_NUMBER: _ClassVar[int]
    MPATH_INDIC_FIELD_NUMBER: _ClassVar[int]
    DOPPLER_MS_FIELD_NUMBER: _ClassVar[int]
    DOPPLER_HZ_FIELD_NUMBER: _ClassVar[int]
    WHOLE_CHIPS_FIELD_NUMBER: _ClassVar[int]
    FRAC_CHIPS_FIELD_NUMBER: _ClassVar[int]
    CODE_PHASE_FIELD_NUMBER: _ClassVar[int]
    INT_CODE_PHASE_FIELD_NUMBER: _ClassVar[int]
    PSEU_RANGE_RMS_ERR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    gnss_id: int
    sv_id: int
    c_no: int
    mpath_indic: int
    doppler_ms: int
    doppler_hz: int
    whole_chips: int
    frac_chips: int
    code_phase: int
    int_code_phase: int
    pseu_range_rms_err: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., gnss_id: _Optional[int] = ..., sv_id: _Optional[int] = ..., c_no: _Optional[int] = ..., mpath_indic: _Optional[int] = ..., doppler_ms: _Optional[int] = ..., doppler_hz: _Optional[int] = ..., whole_chips: _Optional[int] = ..., frac_chips: _Optional[int] = ..., code_phase: _Optional[int] = ..., int_code_phase: _Optional[int] = ..., pseu_range_rms_err: _Optional[int] = ...) -> None: ...
