from google.protobuf import any_pb2 as _any_pb2
from nvidia_ace import animation_pb2 as _animation_pb2
from nvidia_ace import audio_pb2 as _audio_pb2
from nvidia_ace import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    END_OF_A2F_AUDIO_PROCESSING: _ClassVar[EventType]
END_OF_A2F_AUDIO_PROCESSING: EventType

class AudioWithEmotionStream(_message.Message):
    __slots__ = ("audio_stream_header", "audio_with_emotion", "end_of_audio")
    class EndOfAudio(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    AUDIO_STREAM_HEADER_FIELD_NUMBER: _ClassVar[int]
    AUDIO_WITH_EMOTION_FIELD_NUMBER: _ClassVar[int]
    END_OF_AUDIO_FIELD_NUMBER: _ClassVar[int]
    audio_stream_header: AudioWithEmotionStreamHeader
    audio_with_emotion: AudioWithEmotion
    end_of_audio: AudioWithEmotionStream.EndOfAudio
    def __init__(self, audio_stream_header: _Optional[_Union[AudioWithEmotionStreamHeader, _Mapping]] = ..., audio_with_emotion: _Optional[_Union[AudioWithEmotion, _Mapping]] = ..., end_of_audio: _Optional[_Union[AudioWithEmotionStream.EndOfAudio, _Mapping]] = ...) -> None: ...

class AudioWithEmotionStreamHeader(_message.Message):
    __slots__ = ("audio_header", "face_params", "emotion_post_processing_params", "blendshape_params", "emotion_params")
    AUDIO_HEADER_FIELD_NUMBER: _ClassVar[int]
    FACE_PARAMS_FIELD_NUMBER: _ClassVar[int]
    EMOTION_POST_PROCESSING_PARAMS_FIELD_NUMBER: _ClassVar[int]
    BLENDSHAPE_PARAMS_FIELD_NUMBER: _ClassVar[int]
    EMOTION_PARAMS_FIELD_NUMBER: _ClassVar[int]
    audio_header: _audio_pb2.AudioHeader
    face_params: FaceParameters
    emotion_post_processing_params: EmotionPostProcessingParameters
    blendshape_params: BlendShapeParameters
    emotion_params: EmotionParameters
    def __init__(self, audio_header: _Optional[_Union[_audio_pb2.AudioHeader, _Mapping]] = ..., face_params: _Optional[_Union[FaceParameters, _Mapping]] = ..., emotion_post_processing_params: _Optional[_Union[EmotionPostProcessingParameters, _Mapping]] = ..., blendshape_params: _Optional[_Union[BlendShapeParameters, _Mapping]] = ..., emotion_params: _Optional[_Union[EmotionParameters, _Mapping]] = ...) -> None: ...

class Event(_message.Message):
    __slots__ = ("event_type", "metadata")
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    event_type: EventType
    metadata: _any_pb2.Any
    def __init__(self, event_type: _Optional[_Union[EventType, str]] = ..., metadata: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class A2F3DAnimationDataStreamHeader(_message.Message):
    __slots__ = ("audio_header", "skel_animation_header", "start_time_code_since_epoch")
    AUDIO_HEADER_FIELD_NUMBER: _ClassVar[int]
    SKEL_ANIMATION_HEADER_FIELD_NUMBER: _ClassVar[int]
    START_TIME_CODE_SINCE_EPOCH_FIELD_NUMBER: _ClassVar[int]
    audio_header: _audio_pb2.AudioHeader
    skel_animation_header: _animation_pb2.SkelAnimationHeader
    start_time_code_since_epoch: float
    def __init__(self, audio_header: _Optional[_Union[_audio_pb2.AudioHeader, _Mapping]] = ..., skel_animation_header: _Optional[_Union[_animation_pb2.SkelAnimationHeader, _Mapping]] = ..., start_time_code_since_epoch: _Optional[float] = ...) -> None: ...

class A2F3DAnimationDataStream(_message.Message):
    __slots__ = ("animation_data_stream_header", "animation_data", "event", "status")
    ANIMATION_DATA_STREAM_HEADER_FIELD_NUMBER: _ClassVar[int]
    ANIMATION_DATA_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    animation_data_stream_header: A2F3DAnimationDataStreamHeader
    animation_data: _animation_pb2.AnimationData
    event: Event
    status: _status_pb2.Status
    def __init__(self, animation_data_stream_header: _Optional[_Union[A2F3DAnimationDataStreamHeader, _Mapping]] = ..., animation_data: _Optional[_Union[_animation_pb2.AnimationData, _Mapping]] = ..., event: _Optional[_Union[Event, _Mapping]] = ..., status: _Optional[_Union[_status_pb2.Status, _Mapping]] = ...) -> None: ...

class FloatArray(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, values: _Optional[_Iterable[float]] = ...) -> None: ...

class FaceParameters(_message.Message):
    __slots__ = ("float_params", "integer_params", "float_array_params")
    class FloatParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    class IntegerParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    class FloatArrayParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: FloatArray
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[FloatArray, _Mapping]] = ...) -> None: ...
    FLOAT_PARAMS_FIELD_NUMBER: _ClassVar[int]
    INTEGER_PARAMS_FIELD_NUMBER: _ClassVar[int]
    FLOAT_ARRAY_PARAMS_FIELD_NUMBER: _ClassVar[int]
    float_params: _containers.ScalarMap[str, float]
    integer_params: _containers.ScalarMap[str, int]
    float_array_params: _containers.MessageMap[str, FloatArray]
    def __init__(self, float_params: _Optional[_Mapping[str, float]] = ..., integer_params: _Optional[_Mapping[str, int]] = ..., float_array_params: _Optional[_Mapping[str, FloatArray]] = ...) -> None: ...

class BlendShapeParameters(_message.Message):
    __slots__ = ("bs_weight_multipliers", "bs_weight_offsets", "enable_clamping_bs_weight")
    class BsWeightMultipliersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    class BsWeightOffsetsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    BS_WEIGHT_MULTIPLIERS_FIELD_NUMBER: _ClassVar[int]
    BS_WEIGHT_OFFSETS_FIELD_NUMBER: _ClassVar[int]
    ENABLE_CLAMPING_BS_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    bs_weight_multipliers: _containers.ScalarMap[str, float]
    bs_weight_offsets: _containers.ScalarMap[str, float]
    enable_clamping_bs_weight: bool
    def __init__(self, bs_weight_multipliers: _Optional[_Mapping[str, float]] = ..., bs_weight_offsets: _Optional[_Mapping[str, float]] = ..., enable_clamping_bs_weight: bool = ...) -> None: ...

class EmotionParameters(_message.Message):
    __slots__ = ("live_transition_time", "beginning_emotion")
    class BeginningEmotionEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    LIVE_TRANSITION_TIME_FIELD_NUMBER: _ClassVar[int]
    BEGINNING_EMOTION_FIELD_NUMBER: _ClassVar[int]
    live_transition_time: float
    beginning_emotion: _containers.ScalarMap[str, float]
    def __init__(self, live_transition_time: _Optional[float] = ..., beginning_emotion: _Optional[_Mapping[str, float]] = ...) -> None: ...

class EmotionPostProcessingParameters(_message.Message):
    __slots__ = ("emotion_contrast", "live_blend_coef", "enable_preferred_emotion", "preferred_emotion_strength", "emotion_strength", "max_emotions")
    EMOTION_CONTRAST_FIELD_NUMBER: _ClassVar[int]
    LIVE_BLEND_COEF_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PREFERRED_EMOTION_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_EMOTION_STRENGTH_FIELD_NUMBER: _ClassVar[int]
    EMOTION_STRENGTH_FIELD_NUMBER: _ClassVar[int]
    MAX_EMOTIONS_FIELD_NUMBER: _ClassVar[int]
    emotion_contrast: float
    live_blend_coef: float
    enable_preferred_emotion: bool
    preferred_emotion_strength: float
    emotion_strength: float
    max_emotions: int
    def __init__(self, emotion_contrast: _Optional[float] = ..., live_blend_coef: _Optional[float] = ..., enable_preferred_emotion: bool = ..., preferred_emotion_strength: _Optional[float] = ..., emotion_strength: _Optional[float] = ..., max_emotions: _Optional[int] = ...) -> None: ...

class AudioWithEmotion(_message.Message):
    __slots__ = ("audio_buffer", "emotions")
    AUDIO_BUFFER_FIELD_NUMBER: _ClassVar[int]
    EMOTIONS_FIELD_NUMBER: _ClassVar[int]
    audio_buffer: bytes
    emotions: _containers.RepeatedCompositeFieldContainer[EmotionWithTimeCode]
    def __init__(self, audio_buffer: _Optional[bytes] = ..., emotions: _Optional[_Iterable[_Union[EmotionWithTimeCode, _Mapping]]] = ...) -> None: ...

class EmotionWithTimeCode(_message.Message):
    __slots__ = ("time_code", "emotion")
    class EmotionEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    TIME_CODE_FIELD_NUMBER: _ClassVar[int]
    EMOTION_FIELD_NUMBER: _ClassVar[int]
    time_code: float
    emotion: _containers.ScalarMap[str, float]
    def __init__(self, time_code: _Optional[float] = ..., emotion: _Optional[_Mapping[str, float]] = ...) -> None: ...

class EmotionAggregate(_message.Message):
    __slots__ = ("input_emotions", "a2e_output", "a2f_smoothed_output")
    INPUT_EMOTIONS_FIELD_NUMBER: _ClassVar[int]
    A2E_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    A2F_SMOOTHED_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    input_emotions: _containers.RepeatedCompositeFieldContainer[EmotionWithTimeCode]
    a2e_output: _containers.RepeatedCompositeFieldContainer[EmotionWithTimeCode]
    a2f_smoothed_output: _containers.RepeatedCompositeFieldContainer[EmotionWithTimeCode]
    def __init__(self, input_emotions: _Optional[_Iterable[_Union[EmotionWithTimeCode, _Mapping]]] = ..., a2e_output: _Optional[_Iterable[_Union[EmotionWithTimeCode, _Mapping]]] = ..., a2f_smoothed_output: _Optional[_Iterable[_Union[EmotionWithTimeCode, _Mapping]]] = ...) -> None: ...
