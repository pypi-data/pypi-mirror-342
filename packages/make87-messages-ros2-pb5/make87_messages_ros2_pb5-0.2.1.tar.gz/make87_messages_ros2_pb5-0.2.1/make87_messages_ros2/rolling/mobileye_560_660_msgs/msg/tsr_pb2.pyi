from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Tsr(_message.Message):
    __slots__ = ("header", "vision_only_sign_type", "vision_only_supplementary_sign_type", "sign_position_x", "sign_position_y", "sign_position_z", "filter_type")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VISION_ONLY_SIGN_TYPE_FIELD_NUMBER: _ClassVar[int]
    VISION_ONLY_SUPPLEMENTARY_SIGN_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIGN_POSITION_X_FIELD_NUMBER: _ClassVar[int]
    SIGN_POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    SIGN_POSITION_Z_FIELD_NUMBER: _ClassVar[int]
    FILTER_TYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    vision_only_sign_type: int
    vision_only_supplementary_sign_type: int
    sign_position_x: float
    sign_position_y: float
    sign_position_z: float
    filter_type: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., vision_only_sign_type: _Optional[int] = ..., vision_only_supplementary_sign_type: _Optional[int] = ..., sign_position_x: _Optional[float] = ..., sign_position_y: _Optional[float] = ..., sign_position_z: _Optional[float] = ..., filter_type: _Optional[int] = ...) -> None: ...
