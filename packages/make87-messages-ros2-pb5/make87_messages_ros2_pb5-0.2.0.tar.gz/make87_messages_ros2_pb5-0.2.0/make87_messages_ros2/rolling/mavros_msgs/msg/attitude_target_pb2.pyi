from make87_messages_ros2.rolling.geometry_msgs.msg import quaternion_pb2 as _quaternion_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AttitudeTarget(_message.Message):
    __slots__ = ("header", "type_mask", "orientation", "body_rate", "thrust")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_MASK_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    BODY_RATE_FIELD_NUMBER: _ClassVar[int]
    THRUST_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    type_mask: int
    orientation: _quaternion_pb2.Quaternion
    body_rate: _vector3_pb2.Vector3
    thrust: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., type_mask: _Optional[int] = ..., orientation: _Optional[_Union[_quaternion_pb2.Quaternion, _Mapping]] = ..., body_rate: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., thrust: _Optional[float] = ...) -> None: ...
