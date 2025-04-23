from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import transform_pb2 as _transform_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddStaticTransformRequest(_message.Message):
    __slots__ = ("header", "frame_id", "child_frame_id", "transform")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    CHILD_FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    frame_id: str
    child_frame_id: str
    transform: _transform_pb2.Transform
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., frame_id: _Optional[str] = ..., child_frame_id: _Optional[str] = ..., transform: _Optional[_Union[_transform_pb2.Transform, _Mapping]] = ...) -> None: ...

class AddStaticTransformResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
