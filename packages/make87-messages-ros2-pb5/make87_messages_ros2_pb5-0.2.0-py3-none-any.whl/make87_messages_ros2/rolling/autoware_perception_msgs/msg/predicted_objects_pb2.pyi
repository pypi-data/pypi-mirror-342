from make87_messages_ros2.rolling.autoware_perception_msgs.msg import predicted_object_pb2 as _predicted_object_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PredictedObjects(_message.Message):
    __slots__ = ("header", "objects")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    objects: _containers.RepeatedCompositeFieldContainer[_predicted_object_pb2.PredictedObject]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., objects: _Optional[_Iterable[_Union[_predicted_object_pb2.PredictedObject, _Mapping]]] = ...) -> None: ...
