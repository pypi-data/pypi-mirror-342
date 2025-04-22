from libuseful.exception import *
from libuseful.lib_logger import *
from _typeshed import Incomplete

logger: Incomplete

class TouchType:
    DOWN: str
    DOWN_MULTI: str
    UP: str
    UP_MULTI: str
    MOVE: str

class CTProperty:
    @property
    def uptime(self): ...
    @property
    def slot(self): ...
    @property
    def touchType(self): ...
    @property
    def x(self): ...
    @property
    def y(self): ...
    def __init__(self, slot: int, uptime: float, ttype: TouchType, x: int, y: int) -> None: ...
    def __del__(self) -> None: ...
