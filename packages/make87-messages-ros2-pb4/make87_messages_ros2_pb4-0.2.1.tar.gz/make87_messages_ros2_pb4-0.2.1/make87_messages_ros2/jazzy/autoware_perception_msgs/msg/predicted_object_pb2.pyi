from make87_messages_ros2.jazzy.autoware_perception_msgs.msg import object_classification_pb2 as _object_classification_pb2
from make87_messages_ros2.jazzy.autoware_perception_msgs.msg import predicted_object_kinematics_pb2 as _predicted_object_kinematics_pb2
from make87_messages_ros2.jazzy.autoware_perception_msgs.msg import shape_pb2 as _shape_pb2
from make87_messages_ros2.jazzy.unique_identifier_msgs.msg import uuid_pb2 as _uuid_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PredictedObject(_message.Message):
    __slots__ = ["object_id", "existence_probability", "classification", "kinematics", "shape"]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    EXISTENCE_PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    KINEMATICS_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    object_id: _uuid_pb2.UUID
    existence_probability: float
    classification: _containers.RepeatedCompositeFieldContainer[_object_classification_pb2.ObjectClassification]
    kinematics: _predicted_object_kinematics_pb2.PredictedObjectKinematics
    shape: _shape_pb2.Shape
    def __init__(self, object_id: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., existence_probability: _Optional[float] = ..., classification: _Optional[_Iterable[_Union[_object_classification_pb2.ObjectClassification, _Mapping]]] = ..., kinematics: _Optional[_Union[_predicted_object_kinematics_pb2.PredictedObjectKinematics, _Mapping]] = ..., shape: _Optional[_Union[_shape_pb2.Shape, _Mapping]] = ...) -> None: ...
