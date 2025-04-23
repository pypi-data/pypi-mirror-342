from make87_messages_ros2.jazzy.rtabmap_msgs.msg import map_data_pb2 as _map_data_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetMap2Request(_message.Message):
    __slots__ = ("global_map", "optimized", "with_images", "with_scans", "with_user_data", "with_grids", "with_words", "with_global_descriptors")
    GLOBAL_MAP_FIELD_NUMBER: _ClassVar[int]
    OPTIMIZED_FIELD_NUMBER: _ClassVar[int]
    WITH_IMAGES_FIELD_NUMBER: _ClassVar[int]
    WITH_SCANS_FIELD_NUMBER: _ClassVar[int]
    WITH_USER_DATA_FIELD_NUMBER: _ClassVar[int]
    WITH_GRIDS_FIELD_NUMBER: _ClassVar[int]
    WITH_WORDS_FIELD_NUMBER: _ClassVar[int]
    WITH_GLOBAL_DESCRIPTORS_FIELD_NUMBER: _ClassVar[int]
    global_map: bool
    optimized: bool
    with_images: bool
    with_scans: bool
    with_user_data: bool
    with_grids: bool
    with_words: bool
    with_global_descriptors: bool
    def __init__(self, global_map: bool = ..., optimized: bool = ..., with_images: bool = ..., with_scans: bool = ..., with_user_data: bool = ..., with_grids: bool = ..., with_words: bool = ..., with_global_descriptors: bool = ...) -> None: ...

class GetMap2Response(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _map_data_pb2.MapData
    def __init__(self, data: _Optional[_Union[_map_data_pb2.MapData, _Mapping]] = ...) -> None: ...
