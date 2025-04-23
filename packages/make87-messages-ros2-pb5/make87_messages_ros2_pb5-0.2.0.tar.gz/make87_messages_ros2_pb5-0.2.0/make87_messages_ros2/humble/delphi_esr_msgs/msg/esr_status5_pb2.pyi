from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsrStatus5(_message.Message):
    __slots__ = ("header", "ros2_header", "canmsg", "swbatt_a2d", "ignp_a2d", "temp1_a2d", "temp2_a2d", "supply_5va_a2d", "supply_5vdx_a2d", "supply_3p3v_a2d", "supply_10v_a2d")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CANMSG_FIELD_NUMBER: _ClassVar[int]
    SWBATT_A2D_FIELD_NUMBER: _ClassVar[int]
    IGNP_A2D_FIELD_NUMBER: _ClassVar[int]
    TEMP1_A2D_FIELD_NUMBER: _ClassVar[int]
    TEMP2_A2D_FIELD_NUMBER: _ClassVar[int]
    SUPPLY_5VA_A2D_FIELD_NUMBER: _ClassVar[int]
    SUPPLY_5VDX_A2D_FIELD_NUMBER: _ClassVar[int]
    SUPPLY_3P3V_A2D_FIELD_NUMBER: _ClassVar[int]
    SUPPLY_10V_A2D_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    canmsg: str
    swbatt_a2d: int
    ignp_a2d: int
    temp1_a2d: int
    temp2_a2d: int
    supply_5va_a2d: int
    supply_5vdx_a2d: int
    supply_3p3v_a2d: int
    supply_10v_a2d: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., canmsg: _Optional[str] = ..., swbatt_a2d: _Optional[int] = ..., ignp_a2d: _Optional[int] = ..., temp1_a2d: _Optional[int] = ..., temp2_a2d: _Optional[int] = ..., supply_5va_a2d: _Optional[int] = ..., supply_5vdx_a2d: _Optional[int] = ..., supply_3p3v_a2d: _Optional[int] = ..., supply_10v_a2d: _Optional[int] = ...) -> None: ...
