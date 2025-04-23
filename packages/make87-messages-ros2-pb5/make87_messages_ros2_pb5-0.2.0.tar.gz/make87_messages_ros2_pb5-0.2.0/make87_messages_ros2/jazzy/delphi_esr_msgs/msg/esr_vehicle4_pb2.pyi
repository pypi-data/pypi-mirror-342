from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsrVehicle4(_message.Message):
    __slots__ = ("header", "fac_align_cmd_1", "fac_align_cmd_2", "fac_align_max_nt", "fac_align_samp_req", "fac_tgt_mtg_offset", "fac_tgt_mtg_space_hor", "fac_tgt_mtg_space_ver", "fac_tgt_range_1", "fac_tgt_range_r2m", "fac_tgt_range_m2t")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FAC_ALIGN_CMD_1_FIELD_NUMBER: _ClassVar[int]
    FAC_ALIGN_CMD_2_FIELD_NUMBER: _ClassVar[int]
    FAC_ALIGN_MAX_NT_FIELD_NUMBER: _ClassVar[int]
    FAC_ALIGN_SAMP_REQ_FIELD_NUMBER: _ClassVar[int]
    FAC_TGT_MTG_OFFSET_FIELD_NUMBER: _ClassVar[int]
    FAC_TGT_MTG_SPACE_HOR_FIELD_NUMBER: _ClassVar[int]
    FAC_TGT_MTG_SPACE_VER_FIELD_NUMBER: _ClassVar[int]
    FAC_TGT_RANGE_1_FIELD_NUMBER: _ClassVar[int]
    FAC_TGT_RANGE_R2M_FIELD_NUMBER: _ClassVar[int]
    FAC_TGT_RANGE_M2T_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    fac_align_cmd_1: bool
    fac_align_cmd_2: bool
    fac_align_max_nt: int
    fac_align_samp_req: int
    fac_tgt_mtg_offset: int
    fac_tgt_mtg_space_hor: int
    fac_tgt_mtg_space_ver: int
    fac_tgt_range_1: float
    fac_tgt_range_r2m: float
    fac_tgt_range_m2t: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., fac_align_cmd_1: bool = ..., fac_align_cmd_2: bool = ..., fac_align_max_nt: _Optional[int] = ..., fac_align_samp_req: _Optional[int] = ..., fac_tgt_mtg_offset: _Optional[int] = ..., fac_tgt_mtg_space_hor: _Optional[int] = ..., fac_tgt_mtg_space_ver: _Optional[int] = ..., fac_tgt_range_1: _Optional[float] = ..., fac_tgt_range_r2m: _Optional[float] = ..., fac_tgt_range_m2t: _Optional[float] = ...) -> None: ...
