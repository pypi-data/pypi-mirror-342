from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ublox_msgs.msg import cfg_valset_cfgdata_pb2 as _cfg_valset_cfgdata_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CfgVALSET(_message.Message):
    __slots__ = ("header", "version", "layers", "reserved0", "cfgdata")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    CFGDATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    version: int
    layers: int
    reserved0: _containers.RepeatedScalarFieldContainer[int]
    cfgdata: _containers.RepeatedCompositeFieldContainer[_cfg_valset_cfgdata_pb2.CfgVALSETCfgdata]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., version: _Optional[int] = ..., layers: _Optional[int] = ..., reserved0: _Optional[_Iterable[int]] = ..., cfgdata: _Optional[_Iterable[_Union[_cfg_valset_cfgdata_pb2.CfgVALSETCfgdata, _Mapping]]] = ...) -> None: ...
