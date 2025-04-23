from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SrrStatus4(_message.Message):
    __slots__ = ("header", "can_tx_sw_version_host", "can_tx_path_id_blis_ignore", "can_tx_path_id_blis", "can_tx_angle_misalignment", "can_tx_auto_align_angle")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_SW_VERSION_HOST_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_PATH_ID_BLIS_IGNORE_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_PATH_ID_BLIS_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_ANGLE_MISALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_AUTO_ALIGN_ANGLE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    can_tx_sw_version_host: int
    can_tx_path_id_blis_ignore: int
    can_tx_path_id_blis: int
    can_tx_angle_misalignment: float
    can_tx_auto_align_angle: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., can_tx_sw_version_host: _Optional[int] = ..., can_tx_path_id_blis_ignore: _Optional[int] = ..., can_tx_path_id_blis: _Optional[int] = ..., can_tx_angle_misalignment: _Optional[float] = ..., can_tx_auto_align_angle: _Optional[float] = ...) -> None: ...
