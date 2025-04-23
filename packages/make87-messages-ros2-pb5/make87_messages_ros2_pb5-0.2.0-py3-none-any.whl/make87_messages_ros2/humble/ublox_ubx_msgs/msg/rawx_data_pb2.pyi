from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ublox_ubx_msgs.msg import trk_stat_pb2 as _trk_stat_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RawxData(_message.Message):
    __slots__ = ("header", "pr_mes", "cp_mes", "do_mes", "gnss_id", "sv_id", "sig_id", "freq_id", "locktime", "c_no", "pr_stdev", "cp_stdev", "do_stdev", "trk_stat")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PR_MES_FIELD_NUMBER: _ClassVar[int]
    CP_MES_FIELD_NUMBER: _ClassVar[int]
    DO_MES_FIELD_NUMBER: _ClassVar[int]
    GNSS_ID_FIELD_NUMBER: _ClassVar[int]
    SV_ID_FIELD_NUMBER: _ClassVar[int]
    SIG_ID_FIELD_NUMBER: _ClassVar[int]
    FREQ_ID_FIELD_NUMBER: _ClassVar[int]
    LOCKTIME_FIELD_NUMBER: _ClassVar[int]
    C_NO_FIELD_NUMBER: _ClassVar[int]
    PR_STDEV_FIELD_NUMBER: _ClassVar[int]
    CP_STDEV_FIELD_NUMBER: _ClassVar[int]
    DO_STDEV_FIELD_NUMBER: _ClassVar[int]
    TRK_STAT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pr_mes: float
    cp_mes: float
    do_mes: float
    gnss_id: int
    sv_id: int
    sig_id: int
    freq_id: int
    locktime: int
    c_no: int
    pr_stdev: int
    cp_stdev: int
    do_stdev: int
    trk_stat: _trk_stat_pb2.TrkStat
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pr_mes: _Optional[float] = ..., cp_mes: _Optional[float] = ..., do_mes: _Optional[float] = ..., gnss_id: _Optional[int] = ..., sv_id: _Optional[int] = ..., sig_id: _Optional[int] = ..., freq_id: _Optional[int] = ..., locktime: _Optional[int] = ..., c_no: _Optional[int] = ..., pr_stdev: _Optional[int] = ..., cp_stdev: _Optional[int] = ..., do_stdev: _Optional[int] = ..., trk_stat: _Optional[_Union[_trk_stat_pb2.TrkStat, _Mapping]] = ...) -> None: ...
