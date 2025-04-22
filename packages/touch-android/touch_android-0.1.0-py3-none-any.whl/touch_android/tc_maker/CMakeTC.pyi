from libuseful.exception import *
from libuseful.lib_logger import *
from .CPropTouch import CPropSheet as CPropSheet, CPropTouch as CPropTouch
from _typeshed import Incomplete

logger: Incomplete

class CMakeTC:
    def make(self, alias: str, context: CPropTouch) -> tuple[str, str]: ...
    def __init__(self, out_root: str, module_name: str = 'unknown') -> None: ...
    def __del__(self) -> None: ...
