from make87_messages_ros2.jazzy.ublox_msgs.msg import cfg_inf_block_pb2 as _cfg_inf_block_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CfgINF(_message.Message):
    __slots__ = ("blocks",)
    BLOCKS_FIELD_NUMBER: _ClassVar[int]
    blocks: _containers.RepeatedCompositeFieldContainer[_cfg_inf_block_pb2.CfgINFBlock]
    def __init__(self, blocks: _Optional[_Iterable[_Union[_cfg_inf_block_pb2.CfgINFBlock, _Mapping]]] = ...) -> None: ...
