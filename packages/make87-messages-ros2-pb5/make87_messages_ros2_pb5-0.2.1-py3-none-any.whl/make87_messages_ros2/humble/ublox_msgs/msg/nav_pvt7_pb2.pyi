from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NavPVT7(_message.Message):
    __slots__ = ("header", "i_tow", "year", "month", "day", "hour", "min", "sec", "valid", "t_acc", "nano", "fix_type", "flags", "flags2", "num_sv", "lon", "lat", "height", "h_msl", "h_acc", "v_acc", "vel_n", "vel_e", "vel_d", "g_speed", "heading", "s_acc", "head_acc", "p_dop", "reserved1")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    MONTH_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    HOUR_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    SEC_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    T_ACC_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    FIX_TYPE_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    FLAGS2_FIELD_NUMBER: _ClassVar[int]
    NUM_SV_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    H_MSL_FIELD_NUMBER: _ClassVar[int]
    H_ACC_FIELD_NUMBER: _ClassVar[int]
    V_ACC_FIELD_NUMBER: _ClassVar[int]
    VEL_N_FIELD_NUMBER: _ClassVar[int]
    VEL_E_FIELD_NUMBER: _ClassVar[int]
    VEL_D_FIELD_NUMBER: _ClassVar[int]
    G_SPEED_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    S_ACC_FIELD_NUMBER: _ClassVar[int]
    HEAD_ACC_FIELD_NUMBER: _ClassVar[int]
    P_DOP_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    i_tow: int
    year: int
    month: int
    day: int
    hour: int
    min: int
    sec: int
    valid: int
    t_acc: int
    nano: int
    fix_type: int
    flags: int
    flags2: int
    num_sv: int
    lon: int
    lat: int
    height: int
    h_msl: int
    h_acc: int
    v_acc: int
    vel_n: int
    vel_e: int
    vel_d: int
    g_speed: int
    heading: int
    s_acc: int
    head_acc: int
    p_dop: int
    reserved1: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., i_tow: _Optional[int] = ..., year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ..., hour: _Optional[int] = ..., min: _Optional[int] = ..., sec: _Optional[int] = ..., valid: _Optional[int] = ..., t_acc: _Optional[int] = ..., nano: _Optional[int] = ..., fix_type: _Optional[int] = ..., flags: _Optional[int] = ..., flags2: _Optional[int] = ..., num_sv: _Optional[int] = ..., lon: _Optional[int] = ..., lat: _Optional[int] = ..., height: _Optional[int] = ..., h_msl: _Optional[int] = ..., h_acc: _Optional[int] = ..., v_acc: _Optional[int] = ..., vel_n: _Optional[int] = ..., vel_e: _Optional[int] = ..., vel_d: _Optional[int] = ..., g_speed: _Optional[int] = ..., heading: _Optional[int] = ..., s_acc: _Optional[int] = ..., head_acc: _Optional[int] = ..., p_dop: _Optional[int] = ..., reserved1: _Optional[_Iterable[int]] = ...) -> None: ...
