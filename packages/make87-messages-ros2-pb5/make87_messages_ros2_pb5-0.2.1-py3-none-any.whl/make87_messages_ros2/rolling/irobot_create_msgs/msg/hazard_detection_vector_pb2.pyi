from make87_messages_ros2.rolling.irobot_create_msgs.msg import hazard_detection_pb2 as _hazard_detection_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HazardDetectionVector(_message.Message):
    __slots__ = ("header", "detections")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DETECTIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    detections: _containers.RepeatedCompositeFieldContainer[_hazard_detection_pb2.HazardDetection]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., detections: _Optional[_Iterable[_Union[_hazard_detection_pb2.HazardDetection, _Mapping]]] = ...) -> None: ...
