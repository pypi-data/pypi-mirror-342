import blsct
from .managed_obj import ManagedObj
from typing import Any, Self, override

class Script(ManagedObj):
  def value(self) -> Any:
    return blsct.cast_to_uint8_t_ptr(self.obj)

  def to_hex(self) -> str:
    buf = blsct.cast_to_uint8_t_ptr(self.value())
    return blsct.to_hex(buf, blsct.SCRIPT_SIZE)

