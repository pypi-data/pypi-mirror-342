from make87_messages_ros2.jazzy.std_msgs.msg import color_rgba_pb2 as _color_rgba_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetLightPropertiesRequest(_message.Message):
    __slots__ = ("light_name", "diffuse", "attenuation_constant", "attenuation_linear", "attenuation_quadratic")
    LIGHT_NAME_FIELD_NUMBER: _ClassVar[int]
    DIFFUSE_FIELD_NUMBER: _ClassVar[int]
    ATTENUATION_CONSTANT_FIELD_NUMBER: _ClassVar[int]
    ATTENUATION_LINEAR_FIELD_NUMBER: _ClassVar[int]
    ATTENUATION_QUADRATIC_FIELD_NUMBER: _ClassVar[int]
    light_name: str
    diffuse: _color_rgba_pb2.ColorRGBA
    attenuation_constant: float
    attenuation_linear: float
    attenuation_quadratic: float
    def __init__(self, light_name: _Optional[str] = ..., diffuse: _Optional[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]] = ..., attenuation_constant: _Optional[float] = ..., attenuation_linear: _Optional[float] = ..., attenuation_quadratic: _Optional[float] = ...) -> None: ...

class SetLightPropertiesResponse(_message.Message):
    __slots__ = ("success", "status_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status_message: str
    def __init__(self, success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
