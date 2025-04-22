from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class STATUS(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DISCONNECTED: _ClassVar[STATUS]
    IDLE: _ClassVar[STATUS]
    RECORDING: _ClassVar[STATUS]
    RECORD_STOPED: _ClassVar[STATUS]
    PLAYING: _ClassVar[STATUS]
    PLAY_STOPED: _ClassVar[STATUS]
    ERROR: _ClassVar[STATUS]
    BLOCKED: _ClassVar[STATUS]
    RESET: _ClassVar[STATUS]

class ERRNO(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_ERROR: _ClassVar[ERRNO]
    NOT_CONNECTED: _ClassVar[ERRNO]
    BUSY: _ClassVar[ERRNO]
    FAIL_REG_SERVICE: _ClassVar[ERRNO]
    UNINTENDED_ERROR: _ClassVar[ERRNO]
DISCONNECTED: STATUS
IDLE: STATUS
RECORDING: STATUS
RECORD_STOPED: STATUS
PLAYING: STATUS
PLAY_STOPED: STATUS
ERROR: STATUS
BLOCKED: STATUS
RESET: STATUS
NO_ERROR: ERRNO
NOT_CONNECTED: ERRNO
BUSY: ERRNO
FAIL_REG_SERVICE: ERRNO
UNINTENDED_ERROR: ERRNO

class BasicReq(_message.Message):
    __slots__ = ("uid",)
    UID_FIELD_NUMBER: _ClassVar[int]
    uid: str
    def __init__(self, uid: _Optional[str] = ...) -> None: ...

class RecordReq(_message.Message):
    __slots__ = ("uid", "path")
    UID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    uid: str
    path: str
    def __init__(self, uid: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class PlayReq(_message.Message):
    __slots__ = ("uid", "tcs_path")
    UID_FIELD_NUMBER: _ClassVar[int]
    TCS_PATH_FIELD_NUMBER: _ClassVar[int]
    uid: str
    tcs_path: str
    def __init__(self, uid: _Optional[str] = ..., tcs_path: _Optional[str] = ...) -> None: ...

class ErrorData(_message.Message):
    __slots__ = ("msg", "errno")
    MSG_FIELD_NUMBER: _ClassVar[int]
    ERRNO_FIELD_NUMBER: _ClassVar[int]
    msg: str
    errno: int
    def __init__(self, msg: _Optional[str] = ..., errno: _Optional[int] = ...) -> None: ...

class BoolResp(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: bool
    def __init__(self, result: bool = ...) -> None: ...

class StatusResp(_message.Message):
    __slots__ = ("err", "state", "msg")
    ERR_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    err: ErrorData
    state: STATUS
    msg: str
    def __init__(self, err: _Optional[_Union[ErrorData, _Mapping]] = ..., state: _Optional[_Union[STATUS, str]] = ..., msg: _Optional[str] = ...) -> None: ...

class RecordResp(_message.Message):
    __slots__ = ("err", "result", "path")
    ERR_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    err: ErrorData
    result: bool
    path: str
    def __init__(self, err: _Optional[_Union[ErrorData, _Mapping]] = ..., result: bool = ..., path: _Optional[str] = ...) -> None: ...

class PlayResp(_message.Message):
    __slots__ = ("err", "result")
    ERR_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    err: ErrorData
    result: bool
    def __init__(self, err: _Optional[_Union[ErrorData, _Mapping]] = ..., result: bool = ...) -> None: ...
