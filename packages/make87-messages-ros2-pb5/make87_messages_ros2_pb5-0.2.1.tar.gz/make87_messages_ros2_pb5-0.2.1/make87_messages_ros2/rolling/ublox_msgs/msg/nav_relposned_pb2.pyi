from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NavRELPOSNED(_message.Message):
    __slots__ = ("version", "reserved0", "ref_station_id", "i_tow", "rel_pos_n", "rel_pos_e", "rel_pos_d", "rel_pos_hpn", "rel_pos_hpe", "rel_pos_hpd", "reserved1", "acc_n", "acc_e", "acc_d", "flags")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    REF_STATION_ID_FIELD_NUMBER: _ClassVar[int]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    REL_POS_N_FIELD_NUMBER: _ClassVar[int]
    REL_POS_E_FIELD_NUMBER: _ClassVar[int]
    REL_POS_D_FIELD_NUMBER: _ClassVar[int]
    REL_POS_HPN_FIELD_NUMBER: _ClassVar[int]
    REL_POS_HPE_FIELD_NUMBER: _ClassVar[int]
    REL_POS_HPD_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    ACC_N_FIELD_NUMBER: _ClassVar[int]
    ACC_E_FIELD_NUMBER: _ClassVar[int]
    ACC_D_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    version: int
    reserved0: int
    ref_station_id: int
    i_tow: int
    rel_pos_n: int
    rel_pos_e: int
    rel_pos_d: int
    rel_pos_hpn: int
    rel_pos_hpe: int
    rel_pos_hpd: int
    reserved1: int
    acc_n: int
    acc_e: int
    acc_d: int
    flags: int
    def __init__(self, version: _Optional[int] = ..., reserved0: _Optional[int] = ..., ref_station_id: _Optional[int] = ..., i_tow: _Optional[int] = ..., rel_pos_n: _Optional[int] = ..., rel_pos_e: _Optional[int] = ..., rel_pos_d: _Optional[int] = ..., rel_pos_hpn: _Optional[int] = ..., rel_pos_hpe: _Optional[int] = ..., rel_pos_hpd: _Optional[int] = ..., reserved1: _Optional[int] = ..., acc_n: _Optional[int] = ..., acc_e: _Optional[int] = ..., acc_d: _Optional[int] = ..., flags: _Optional[int] = ...) -> None: ...
