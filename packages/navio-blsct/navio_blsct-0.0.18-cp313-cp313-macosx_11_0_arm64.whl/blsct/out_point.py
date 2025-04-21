import blsct
from .managed_obj import ManagedObj
from typing import Any, Self, override

class OutPoint(ManagedObj):
  @override
  def value(self) -> Any:
    return blsct.cast_to_out_point(self.obj)

  @staticmethod
  def generate(tx_id: str, out_index: int) -> Self:
    rv = blsct.gen_out_point(tx_id, out_index)
    inst = OutPoint(rv.value)
    blsct.free_obj(rv)
    return inst

