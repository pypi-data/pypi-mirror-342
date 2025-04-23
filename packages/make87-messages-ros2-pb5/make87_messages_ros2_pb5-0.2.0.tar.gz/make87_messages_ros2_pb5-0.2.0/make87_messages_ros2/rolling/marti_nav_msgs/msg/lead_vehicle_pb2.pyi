from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LeadVehicle(_message.Message):
    __slots__ = ("header", "headway_distance", "speed", "heading", "x_pos", "y_pos", "classification", "type")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    HEADWAY_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    X_POS_FIELD_NUMBER: _ClassVar[int]
    Y_POS_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    headway_distance: float
    speed: float
    heading: float
    x_pos: float
    y_pos: float
    classification: int
    type: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., headway_distance: _Optional[float] = ..., speed: _Optional[float] = ..., heading: _Optional[float] = ..., x_pos: _Optional[float] = ..., y_pos: _Optional[float] = ..., classification: _Optional[int] = ..., type: _Optional[int] = ...) -> None: ...
