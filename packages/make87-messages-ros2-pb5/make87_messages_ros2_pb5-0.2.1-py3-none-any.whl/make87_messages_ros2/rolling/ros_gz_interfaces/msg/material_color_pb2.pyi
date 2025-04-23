from make87_messages_ros2.rolling.ros_gz_interfaces.msg import entity_pb2 as _entity_pb2
from make87_messages_ros2.rolling.std_msgs.msg import color_rgba_pb2 as _color_rgba_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MaterialColor(_message.Message):
    __slots__ = ("header", "entity", "ambient", "diffuse", "specular", "emissive", "shininess", "entity_match")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    AMBIENT_FIELD_NUMBER: _ClassVar[int]
    DIFFUSE_FIELD_NUMBER: _ClassVar[int]
    SPECULAR_FIELD_NUMBER: _ClassVar[int]
    EMISSIVE_FIELD_NUMBER: _ClassVar[int]
    SHININESS_FIELD_NUMBER: _ClassVar[int]
    ENTITY_MATCH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    entity: _entity_pb2.Entity
    ambient: _color_rgba_pb2.ColorRGBA
    diffuse: _color_rgba_pb2.ColorRGBA
    specular: _color_rgba_pb2.ColorRGBA
    emissive: _color_rgba_pb2.ColorRGBA
    shininess: float
    entity_match: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., entity: _Optional[_Union[_entity_pb2.Entity, _Mapping]] = ..., ambient: _Optional[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]] = ..., diffuse: _Optional[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]] = ..., specular: _Optional[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]] = ..., emissive: _Optional[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]] = ..., shininess: _Optional[float] = ..., entity_match: _Optional[int] = ...) -> None: ...
