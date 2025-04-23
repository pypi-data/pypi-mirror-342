from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geographic_msgs.msg import geo_pose_pb2 as _geo_pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetDatumRequest(_message.Message):
    __slots__ = ("header", "geo_pose")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GEO_POSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    geo_pose: _geo_pose_pb2.GeoPose
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., geo_pose: _Optional[_Union[_geo_pose_pb2.GeoPose, _Mapping]] = ...) -> None: ...

class SetDatumResponse(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
