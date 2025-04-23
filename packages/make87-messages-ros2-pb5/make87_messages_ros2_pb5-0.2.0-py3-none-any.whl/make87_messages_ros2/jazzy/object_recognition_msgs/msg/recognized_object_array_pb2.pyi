from make87_messages_ros2.jazzy.object_recognition_msgs.msg import recognized_object_pb2 as _recognized_object_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RecognizedObjectArray(_message.Message):
    __slots__ = ("header", "objects", "cooccurrence")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    COOCCURRENCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    objects: _containers.RepeatedCompositeFieldContainer[_recognized_object_pb2.RecognizedObject]
    cooccurrence: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., objects: _Optional[_Iterable[_Union[_recognized_object_pb2.RecognizedObject, _Mapping]]] = ..., cooccurrence: _Optional[_Iterable[float]] = ...) -> None: ...
