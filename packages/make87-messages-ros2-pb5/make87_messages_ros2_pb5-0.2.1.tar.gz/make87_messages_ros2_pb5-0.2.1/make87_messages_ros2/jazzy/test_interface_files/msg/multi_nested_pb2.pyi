from make87_messages_ros2.jazzy.test_interface_files.msg import arrays_pb2 as _arrays_pb2
from make87_messages_ros2.jazzy.test_interface_files.msg import bounded_sequences_pb2 as _bounded_sequences_pb2
from make87_messages_ros2.jazzy.test_interface_files.msg import unbounded_sequences_pb2 as _unbounded_sequences_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MultiNested(_message.Message):
    __slots__ = ("array_of_arrays", "array_of_bounded_sequences", "array_of_unbounded_sequences", "bounded_sequence_of_arrays", "bounded_sequence_of_bounded_sequences", "bounded_sequence_of_unbounded_sequences", "unbounded_sequence_of_arrays", "unbounded_sequence_of_bounded_sequences", "unbounded_sequence_of_unbounded_sequences")
    ARRAY_OF_ARRAYS_FIELD_NUMBER: _ClassVar[int]
    ARRAY_OF_BOUNDED_SEQUENCES_FIELD_NUMBER: _ClassVar[int]
    ARRAY_OF_UNBOUNDED_SEQUENCES_FIELD_NUMBER: _ClassVar[int]
    BOUNDED_SEQUENCE_OF_ARRAYS_FIELD_NUMBER: _ClassVar[int]
    BOUNDED_SEQUENCE_OF_BOUNDED_SEQUENCES_FIELD_NUMBER: _ClassVar[int]
    BOUNDED_SEQUENCE_OF_UNBOUNDED_SEQUENCES_FIELD_NUMBER: _ClassVar[int]
    UNBOUNDED_SEQUENCE_OF_ARRAYS_FIELD_NUMBER: _ClassVar[int]
    UNBOUNDED_SEQUENCE_OF_BOUNDED_SEQUENCES_FIELD_NUMBER: _ClassVar[int]
    UNBOUNDED_SEQUENCE_OF_UNBOUNDED_SEQUENCES_FIELD_NUMBER: _ClassVar[int]
    array_of_arrays: _containers.RepeatedCompositeFieldContainer[_arrays_pb2.Arrays]
    array_of_bounded_sequences: _containers.RepeatedCompositeFieldContainer[_bounded_sequences_pb2.BoundedSequences]
    array_of_unbounded_sequences: _containers.RepeatedCompositeFieldContainer[_unbounded_sequences_pb2.UnboundedSequences]
    bounded_sequence_of_arrays: _containers.RepeatedCompositeFieldContainer[_arrays_pb2.Arrays]
    bounded_sequence_of_bounded_sequences: _containers.RepeatedCompositeFieldContainer[_bounded_sequences_pb2.BoundedSequences]
    bounded_sequence_of_unbounded_sequences: _containers.RepeatedCompositeFieldContainer[_unbounded_sequences_pb2.UnboundedSequences]
    unbounded_sequence_of_arrays: _containers.RepeatedCompositeFieldContainer[_arrays_pb2.Arrays]
    unbounded_sequence_of_bounded_sequences: _containers.RepeatedCompositeFieldContainer[_bounded_sequences_pb2.BoundedSequences]
    unbounded_sequence_of_unbounded_sequences: _containers.RepeatedCompositeFieldContainer[_unbounded_sequences_pb2.UnboundedSequences]
    def __init__(self, array_of_arrays: _Optional[_Iterable[_Union[_arrays_pb2.Arrays, _Mapping]]] = ..., array_of_bounded_sequences: _Optional[_Iterable[_Union[_bounded_sequences_pb2.BoundedSequences, _Mapping]]] = ..., array_of_unbounded_sequences: _Optional[_Iterable[_Union[_unbounded_sequences_pb2.UnboundedSequences, _Mapping]]] = ..., bounded_sequence_of_arrays: _Optional[_Iterable[_Union[_arrays_pb2.Arrays, _Mapping]]] = ..., bounded_sequence_of_bounded_sequences: _Optional[_Iterable[_Union[_bounded_sequences_pb2.BoundedSequences, _Mapping]]] = ..., bounded_sequence_of_unbounded_sequences: _Optional[_Iterable[_Union[_unbounded_sequences_pb2.UnboundedSequences, _Mapping]]] = ..., unbounded_sequence_of_arrays: _Optional[_Iterable[_Union[_arrays_pb2.Arrays, _Mapping]]] = ..., unbounded_sequence_of_bounded_sequences: _Optional[_Iterable[_Union[_bounded_sequences_pb2.BoundedSequences, _Mapping]]] = ..., unbounded_sequence_of_unbounded_sequences: _Optional[_Iterable[_Union[_unbounded_sequences_pb2.UnboundedSequences, _Mapping]]] = ...) -> None: ...
