from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.vimbax_camera_msgs.msg import feature_flags_pb2 as _feature_flags_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FeatureInfo(_message.Message):
    __slots__ = ("header", "name", "category", "display_name", "sfnc_namespace", "unit", "data_type", "flags", "polling_time")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    SFNC_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    POLLING_TIME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    category: str
    display_name: str
    sfnc_namespace: str
    unit: str
    data_type: int
    flags: _feature_flags_pb2.FeatureFlags
    polling_time: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., category: _Optional[str] = ..., display_name: _Optional[str] = ..., sfnc_namespace: _Optional[str] = ..., unit: _Optional[str] = ..., data_type: _Optional[int] = ..., flags: _Optional[_Union[_feature_flags_pb2.FeatureFlags, _Mapping]] = ..., polling_time: _Optional[int] = ...) -> None: ...
