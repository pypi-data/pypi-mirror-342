from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXNavCov(_message.Message):
    __slots__ = ("header", "itow", "version", "pos_cor_valid", "vel_cor_valid", "pos_cov_nn", "pos_cov_ne", "pos_cov_nd", "pos_cov_ee", "pos_cov_ed", "pos_cov_dd", "vel_cov_nn", "vel_cov_ne", "vel_cov_nd", "vel_cov_ee", "vel_cov_ed", "vel_cov_dd")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ITOW_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    POS_COR_VALID_FIELD_NUMBER: _ClassVar[int]
    VEL_COR_VALID_FIELD_NUMBER: _ClassVar[int]
    POS_COV_NN_FIELD_NUMBER: _ClassVar[int]
    POS_COV_NE_FIELD_NUMBER: _ClassVar[int]
    POS_COV_ND_FIELD_NUMBER: _ClassVar[int]
    POS_COV_EE_FIELD_NUMBER: _ClassVar[int]
    POS_COV_ED_FIELD_NUMBER: _ClassVar[int]
    POS_COV_DD_FIELD_NUMBER: _ClassVar[int]
    VEL_COV_NN_FIELD_NUMBER: _ClassVar[int]
    VEL_COV_NE_FIELD_NUMBER: _ClassVar[int]
    VEL_COV_ND_FIELD_NUMBER: _ClassVar[int]
    VEL_COV_EE_FIELD_NUMBER: _ClassVar[int]
    VEL_COV_ED_FIELD_NUMBER: _ClassVar[int]
    VEL_COV_DD_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    itow: int
    version: int
    pos_cor_valid: bool
    vel_cor_valid: bool
    pos_cov_nn: float
    pos_cov_ne: float
    pos_cov_nd: float
    pos_cov_ee: float
    pos_cov_ed: float
    pos_cov_dd: float
    vel_cov_nn: float
    vel_cov_ne: float
    vel_cov_nd: float
    vel_cov_ee: float
    vel_cov_ed: float
    vel_cov_dd: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., itow: _Optional[int] = ..., version: _Optional[int] = ..., pos_cor_valid: bool = ..., vel_cor_valid: bool = ..., pos_cov_nn: _Optional[float] = ..., pos_cov_ne: _Optional[float] = ..., pos_cov_nd: _Optional[float] = ..., pos_cov_ee: _Optional[float] = ..., pos_cov_ed: _Optional[float] = ..., pos_cov_dd: _Optional[float] = ..., vel_cov_nn: _Optional[float] = ..., vel_cov_ne: _Optional[float] = ..., vel_cov_nd: _Optional[float] = ..., vel_cov_ee: _Optional[float] = ..., vel_cov_ed: _Optional[float] = ..., vel_cov_dd: _Optional[float] = ...) -> None: ...
