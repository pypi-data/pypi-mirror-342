from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserInputMedia(_message.Message):
    __slots__ = ["header", "btn_vol_up", "btn_vol_down", "btn_mute", "btn_next", "btn_prev", "btn_next_hang_up", "btn_prev_answer", "btn_hang_up", "btn_answer", "btn_play", "btn_pause", "btn_play_pause", "btn_mode"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BTN_VOL_UP_FIELD_NUMBER: _ClassVar[int]
    BTN_VOL_DOWN_FIELD_NUMBER: _ClassVar[int]
    BTN_MUTE_FIELD_NUMBER: _ClassVar[int]
    BTN_NEXT_FIELD_NUMBER: _ClassVar[int]
    BTN_PREV_FIELD_NUMBER: _ClassVar[int]
    BTN_NEXT_HANG_UP_FIELD_NUMBER: _ClassVar[int]
    BTN_PREV_ANSWER_FIELD_NUMBER: _ClassVar[int]
    BTN_HANG_UP_FIELD_NUMBER: _ClassVar[int]
    BTN_ANSWER_FIELD_NUMBER: _ClassVar[int]
    BTN_PLAY_FIELD_NUMBER: _ClassVar[int]
    BTN_PAUSE_FIELD_NUMBER: _ClassVar[int]
    BTN_PLAY_PAUSE_FIELD_NUMBER: _ClassVar[int]
    BTN_MODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    btn_vol_up: bool
    btn_vol_down: bool
    btn_mute: bool
    btn_next: bool
    btn_prev: bool
    btn_next_hang_up: bool
    btn_prev_answer: bool
    btn_hang_up: bool
    btn_answer: bool
    btn_play: bool
    btn_pause: bool
    btn_play_pause: bool
    btn_mode: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., btn_vol_up: bool = ..., btn_vol_down: bool = ..., btn_mute: bool = ..., btn_next: bool = ..., btn_prev: bool = ..., btn_next_hang_up: bool = ..., btn_prev_answer: bool = ..., btn_hang_up: bool = ..., btn_answer: bool = ..., btn_play: bool = ..., btn_pause: bool = ..., btn_play_pause: bool = ..., btn_mode: bool = ...) -> None: ...
