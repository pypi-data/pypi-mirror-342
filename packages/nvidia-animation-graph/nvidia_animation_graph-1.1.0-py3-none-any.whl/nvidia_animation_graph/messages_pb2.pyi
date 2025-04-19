from google.protobuf import any_pb2 as _any_pb2
from nvidia_ace import animation_pb2 as _animation_pb2
from nvidia_ace import audio_pb2 as _audio_pb2
from nvidia_ace import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AnimationDataStream(_message.Message):
    __slots__ = ("animation_data_stream_header", "animation_data", "status")
    ANIMATION_DATA_STREAM_HEADER_FIELD_NUMBER: _ClassVar[int]
    ANIMATION_DATA_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    animation_data_stream_header: AnimationDataStreamHeader
    animation_data: _animation_pb2.AnimationData
    status: _status_pb2.Status
    def __init__(self, animation_data_stream_header: _Optional[_Union[AnimationDataStreamHeader, _Mapping]] = ..., animation_data: _Optional[_Union[_animation_pb2.AnimationData, _Mapping]] = ..., status: _Optional[_Union[_status_pb2.Status, _Mapping]] = ...) -> None: ...

class AnimationIds(_message.Message):
    __slots__ = ("request_id", "stream_id", "target_object_id")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STREAM_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    stream_id: str
    target_object_id: str
    def __init__(self, request_id: _Optional[str] = ..., stream_id: _Optional[str] = ..., target_object_id: _Optional[str] = ...) -> None: ...

class AnimationDataStreamHeader(_message.Message):
    __slots__ = ("animation_ids", "source_service_id", "audio_header", "skel_animation_header", "start_time_code_since_epoch", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _any_pb2.Any
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...
    ANIMATION_IDS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    AUDIO_HEADER_FIELD_NUMBER: _ClassVar[int]
    SKEL_ANIMATION_HEADER_FIELD_NUMBER: _ClassVar[int]
    START_TIME_CODE_SINCE_EPOCH_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    animation_ids: AnimationIds
    source_service_id: str
    audio_header: _audio_pb2.AudioHeader
    skel_animation_header: _animation_pb2.SkelAnimationHeader
    start_time_code_since_epoch: float
    metadata: _containers.MessageMap[str, _any_pb2.Any]
    def __init__(self, animation_ids: _Optional[_Union[AnimationIds, _Mapping]] = ..., source_service_id: _Optional[str] = ..., audio_header: _Optional[_Union[_audio_pb2.AudioHeader, _Mapping]] = ..., skel_animation_header: _Optional[_Union[_animation_pb2.SkelAnimationHeader, _Mapping]] = ..., start_time_code_since_epoch: _Optional[float] = ..., metadata: _Optional[_Mapping[str, _any_pb2.Any]] = ...) -> None: ...
