from make87_messages_ros2.rolling.sick_safetyscanners2_interfaces.msg import intrusion_datum_pb2 as _intrusion_datum_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IntrusionData(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[_intrusion_datum_pb2.IntrusionDatum]
    def __init__(self, data: _Optional[_Iterable[_Union[_intrusion_datum_pb2.IntrusionDatum, _Mapping]]] = ...) -> None: ...
