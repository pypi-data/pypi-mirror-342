from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SrrStatus3(_message.Message):
    __slots__ = ("header", "can_tx_alignment_state", "can_tx_interface_ver_minor", "can_tx_sw_version_arm", "can_tx_hw_version", "can_tx_interface_version", "can_tx_serial_num")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_ALIGNMENT_STATE_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_INTERFACE_VER_MINOR_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_SW_VERSION_ARM_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_HW_VERSION_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_INTERFACE_VERSION_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_SERIAL_NUM_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    can_tx_alignment_state: int
    can_tx_interface_ver_minor: int
    can_tx_sw_version_arm: int
    can_tx_hw_version: int
    can_tx_interface_version: int
    can_tx_serial_num: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., can_tx_alignment_state: _Optional[int] = ..., can_tx_interface_ver_minor: _Optional[int] = ..., can_tx_sw_version_arm: _Optional[int] = ..., can_tx_hw_version: _Optional[int] = ..., can_tx_interface_version: _Optional[int] = ..., can_tx_serial_num: _Optional[int] = ...) -> None: ...
