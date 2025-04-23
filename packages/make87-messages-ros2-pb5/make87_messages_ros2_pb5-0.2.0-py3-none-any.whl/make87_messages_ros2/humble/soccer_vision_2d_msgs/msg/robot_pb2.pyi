from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.soccer_vision_attribute_msgs.msg import confidence_pb2 as _confidence_pb2
from make87_messages_ros2.humble.soccer_vision_attribute_msgs.msg import robot_pb2 as _robot_pb2
from make87_messages_ros2.humble.vision_msgs.msg import bounding_box2_d_pb2 as _bounding_box2_d_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Robot(_message.Message):
    __slots__ = ("header", "bb", "attributes", "confidence")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BB_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    bb: _bounding_box2_d_pb2.BoundingBox2D
    attributes: _robot_pb2.Robot
    confidence: _confidence_pb2.Confidence
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., bb: _Optional[_Union[_bounding_box2_d_pb2.BoundingBox2D, _Mapping]] = ..., attributes: _Optional[_Union[_robot_pb2.Robot, _Mapping]] = ..., confidence: _Optional[_Union[_confidence_pb2.Confidence, _Mapping]] = ...) -> None: ...
