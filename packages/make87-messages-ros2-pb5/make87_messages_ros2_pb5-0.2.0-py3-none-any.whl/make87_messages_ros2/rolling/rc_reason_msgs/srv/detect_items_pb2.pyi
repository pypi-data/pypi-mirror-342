from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.rolling.rc_common_msgs.msg import return_code_pb2 as _return_code_pb2
from make87_messages_ros2.rolling.rc_reason_msgs.msg import compartment_pb2 as _compartment_pb2
from make87_messages_ros2.rolling.rc_reason_msgs.msg import item_pb2 as _item_pb2
from make87_messages_ros2.rolling.rc_reason_msgs.msg import item_model_pb2 as _item_model_pb2
from make87_messages_ros2.rolling.rc_reason_msgs.msg import load_carrier_pb2 as _load_carrier_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DetectItemsRequest(_message.Message):
    __slots__ = ("pose_frame", "region_of_interest_id", "load_carrier_id", "load_carrier_compartment", "item_models", "robot_pose")
    POSE_FRAME_FIELD_NUMBER: _ClassVar[int]
    REGION_OF_INTEREST_ID_FIELD_NUMBER: _ClassVar[int]
    LOAD_CARRIER_ID_FIELD_NUMBER: _ClassVar[int]
    LOAD_CARRIER_COMPARTMENT_FIELD_NUMBER: _ClassVar[int]
    ITEM_MODELS_FIELD_NUMBER: _ClassVar[int]
    ROBOT_POSE_FIELD_NUMBER: _ClassVar[int]
    pose_frame: str
    region_of_interest_id: str
    load_carrier_id: str
    load_carrier_compartment: _compartment_pb2.Compartment
    item_models: _containers.RepeatedCompositeFieldContainer[_item_model_pb2.ItemModel]
    robot_pose: _pose_pb2.Pose
    def __init__(self, pose_frame: _Optional[str] = ..., region_of_interest_id: _Optional[str] = ..., load_carrier_id: _Optional[str] = ..., load_carrier_compartment: _Optional[_Union[_compartment_pb2.Compartment, _Mapping]] = ..., item_models: _Optional[_Iterable[_Union[_item_model_pb2.ItemModel, _Mapping]]] = ..., robot_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ...) -> None: ...

class DetectItemsResponse(_message.Message):
    __slots__ = ("timestamp", "items", "load_carriers", "return_code")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    LOAD_CARRIERS_FIELD_NUMBER: _ClassVar[int]
    RETURN_CODE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _time_pb2.Time
    items: _containers.RepeatedCompositeFieldContainer[_item_pb2.Item]
    load_carriers: _containers.RepeatedCompositeFieldContainer[_load_carrier_pb2.LoadCarrier]
    return_code: _return_code_pb2.ReturnCode
    def __init__(self, timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., items: _Optional[_Iterable[_Union[_item_pb2.Item, _Mapping]]] = ..., load_carriers: _Optional[_Iterable[_Union[_load_carrier_pb2.LoadCarrier, _Mapping]]] = ..., return_code: _Optional[_Union[_return_code_pb2.ReturnCode, _Mapping]] = ...) -> None: ...
