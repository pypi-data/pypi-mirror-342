from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXNavPosECEF(_message.Message):
    __slots__ = ("header", "itow", "ecef_x", "ecef_y", "ecef_z", "p_acc")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ITOW_FIELD_NUMBER: _ClassVar[int]
    ECEF_X_FIELD_NUMBER: _ClassVar[int]
    ECEF_Y_FIELD_NUMBER: _ClassVar[int]
    ECEF_Z_FIELD_NUMBER: _ClassVar[int]
    P_ACC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    itow: int
    ecef_x: int
    ecef_y: int
    ecef_z: int
    p_acc: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., itow: _Optional[int] = ..., ecef_x: _Optional[int] = ..., ecef_y: _Optional[int] = ..., ecef_z: _Optional[int] = ..., p_acc: _Optional[int] = ...) -> None: ...
