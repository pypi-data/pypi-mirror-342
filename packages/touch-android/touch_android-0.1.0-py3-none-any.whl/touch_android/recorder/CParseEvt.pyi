from libuseful.exception import *
from libuseful.lib_logger import *
from .CTProperty import CTProperty as CTProperty, TouchType as TouchType
from _typeshed import Incomplete

logger: Incomplete

class IParseEvt:
    class STATE:
        NOT_DEFINE: str
        START: str
        STOP: str
        MOVE: Incomplete
        DOWN_MULTI: Incomplete
        DOWN: Incomplete
        UP_MULTI: Incomplete
        UP: Incomplete
    class CTrackPos:
        x: int
        y: int
        @property
        def out(self): ...
        def __init__(self, slot_num: int) -> None: ...
        def update(self, uptime: float, x: int = None, y: int = None): ...
    class SYMBOLs:
        SLOT: str
        TOUCH_MAJOR: str
        POS_X: str
        POS_Y: str
        TRACK_ID: str
        BTN_TOUCH: str
        SYN_REPORT: str
    SOF_SYMBOLs: list[str]
    EOF_SYMBOLs: list[str]
    @property
    def curSlot(self): ...
    def reset(self) -> None: ...
    def __init__(self) -> None: ...
    def __del__(self) -> None: ...

class CParseEvt(IParseEvt):
    class SEARCH:
        NULL: int
        DEV: int
        TOUCH_SPEC: int
    DEV_PREFIX: str
    @staticmethod
    def parse_touch_path(lines: list[str]): ...
    def parse(self, lines: list[str]) -> list[CTProperty]: ...
    @staticmethod
    def __proc_mt_slot__(self, status: IParseEvt.STATE, uptime: float, value: str): ...
    @staticmethod
    def __proc_mt_touch_major__(self, status: IParseEvt.STATE, uptime: float, value: str): ...
    @staticmethod
    def __proc_mt_pos_x__(self, status: IParseEvt.STATE, uptime: float, value: str): ...
    @staticmethod
    def __proc_mt_pos_y__(self, status: IParseEvt.STATE, uptime: float, value: str): ...
    @staticmethod
    def __proc_mt_track_id__(self, status: IParseEvt.STATE, uptime: float, value: str): ...
    @staticmethod
    def __proc_btn_touch__(self, status: IParseEvt.STATE, uptime: float, value: str): ...
    @staticmethod
    def __proc_end__(self, status: IParseEvt.STATE, uptime: float, value: str): ...
    PROC_SYMBOLs: dict
    def __init__(self) -> None: ...
    def __del__(self) -> None: ...
