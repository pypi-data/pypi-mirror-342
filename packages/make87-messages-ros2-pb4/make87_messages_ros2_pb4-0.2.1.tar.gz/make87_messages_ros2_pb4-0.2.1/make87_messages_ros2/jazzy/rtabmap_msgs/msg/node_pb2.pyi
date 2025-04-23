from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.jazzy.rtabmap_msgs.msg import key_point_pb2 as _key_point_pb2
from make87_messages_ros2.jazzy.rtabmap_msgs.msg import point3f_pb2 as _point3f_pb2
from make87_messages_ros2.jazzy.rtabmap_msgs.msg import sensor_data_pb2 as _sensor_data_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Node(_message.Message):
    __slots__ = ["id", "map_id", "weight", "stamp", "label", "pose", "word_id_keys", "word_id_values", "word_kpts", "word_pts", "word_descriptors", "data"]
    ID_FIELD_NUMBER: _ClassVar[int]
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    WORD_ID_KEYS_FIELD_NUMBER: _ClassVar[int]
    WORD_ID_VALUES_FIELD_NUMBER: _ClassVar[int]
    WORD_KPTS_FIELD_NUMBER: _ClassVar[int]
    WORD_PTS_FIELD_NUMBER: _ClassVar[int]
    WORD_DESCRIPTORS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    id: int
    map_id: int
    weight: int
    stamp: float
    label: str
    pose: _pose_pb2.Pose
    word_id_keys: _containers.RepeatedScalarFieldContainer[int]
    word_id_values: _containers.RepeatedScalarFieldContainer[int]
    word_kpts: _containers.RepeatedCompositeFieldContainer[_key_point_pb2.KeyPoint]
    word_pts: _containers.RepeatedCompositeFieldContainer[_point3f_pb2.Point3f]
    word_descriptors: _containers.RepeatedScalarFieldContainer[int]
    data: _sensor_data_pb2.SensorData
    def __init__(self, id: _Optional[int] = ..., map_id: _Optional[int] = ..., weight: _Optional[int] = ..., stamp: _Optional[float] = ..., label: _Optional[str] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., word_id_keys: _Optional[_Iterable[int]] = ..., word_id_values: _Optional[_Iterable[int]] = ..., word_kpts: _Optional[_Iterable[_Union[_key_point_pb2.KeyPoint, _Mapping]]] = ..., word_pts: _Optional[_Iterable[_Union[_point3f_pb2.Point3f, _Mapping]]] = ..., word_descriptors: _Optional[_Iterable[int]] = ..., data: _Optional[_Union[_sensor_data_pb2.SensorData, _Mapping]] = ...) -> None: ...
