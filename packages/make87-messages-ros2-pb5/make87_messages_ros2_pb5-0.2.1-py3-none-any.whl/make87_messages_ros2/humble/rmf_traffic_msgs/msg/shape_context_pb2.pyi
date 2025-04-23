from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import convex_shape_context_pb2 as _convex_shape_context_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ShapeContext(_message.Message):
    __slots__ = ("header", "convex_shapes")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONVEX_SHAPES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    convex_shapes: _convex_shape_context_pb2.ConvexShapeContext
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., convex_shapes: _Optional[_Union[_convex_shape_context_pb2.ConvexShapeContext, _Mapping]] = ...) -> None: ...
