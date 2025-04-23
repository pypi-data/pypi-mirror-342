from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import camera_info_pb2 as _camera_info_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetCameraInfoRequest(_message.Message):
    __slots__ = ("header", "camera_info")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAMERA_INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    camera_info: _camera_info_pb2.CameraInfo
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., camera_info: _Optional[_Union[_camera_info_pb2.CameraInfo, _Mapping]] = ...) -> None: ...

class SetCameraInfoResponse(_message.Message):
    __slots__ = ("header", "success", "status_message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    status_message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
