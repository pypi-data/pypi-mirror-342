from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsrStatus4(_message.Message):
    __slots__ = ("header", "canmsg", "truck_target_det", "lr_only_grating_lobe_det", "sidelobe_blockage", "partial_blockage", "mr_lr_mode", "rolling_count_3", "path_id_acc", "path_id_cmbb_move", "path_id_cmbb_stat", "path_id_fcw_move", "path_id_fcw_stat", "auto_align_angle", "path_id_acc_stat")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CANMSG_FIELD_NUMBER: _ClassVar[int]
    TRUCK_TARGET_DET_FIELD_NUMBER: _ClassVar[int]
    LR_ONLY_GRATING_LOBE_DET_FIELD_NUMBER: _ClassVar[int]
    SIDELOBE_BLOCKAGE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_BLOCKAGE_FIELD_NUMBER: _ClassVar[int]
    MR_LR_MODE_FIELD_NUMBER: _ClassVar[int]
    ROLLING_COUNT_3_FIELD_NUMBER: _ClassVar[int]
    PATH_ID_ACC_FIELD_NUMBER: _ClassVar[int]
    PATH_ID_CMBB_MOVE_FIELD_NUMBER: _ClassVar[int]
    PATH_ID_CMBB_STAT_FIELD_NUMBER: _ClassVar[int]
    PATH_ID_FCW_MOVE_FIELD_NUMBER: _ClassVar[int]
    PATH_ID_FCW_STAT_FIELD_NUMBER: _ClassVar[int]
    AUTO_ALIGN_ANGLE_FIELD_NUMBER: _ClassVar[int]
    PATH_ID_ACC_STAT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    canmsg: str
    truck_target_det: bool
    lr_only_grating_lobe_det: bool
    sidelobe_blockage: bool
    partial_blockage: bool
    mr_lr_mode: int
    rolling_count_3: int
    path_id_acc: int
    path_id_cmbb_move: int
    path_id_cmbb_stat: int
    path_id_fcw_move: int
    path_id_fcw_stat: int
    auto_align_angle: float
    path_id_acc_stat: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., canmsg: _Optional[str] = ..., truck_target_det: bool = ..., lr_only_grating_lobe_det: bool = ..., sidelobe_blockage: bool = ..., partial_blockage: bool = ..., mr_lr_mode: _Optional[int] = ..., rolling_count_3: _Optional[int] = ..., path_id_acc: _Optional[int] = ..., path_id_cmbb_move: _Optional[int] = ..., path_id_cmbb_stat: _Optional[int] = ..., path_id_fcw_move: _Optional[int] = ..., path_id_fcw_stat: _Optional[int] = ..., auto_align_angle: _Optional[float] = ..., path_id_acc_stat: _Optional[int] = ...) -> None: ...
