import blsct
from .managed_obj import ManagedObj
from typing import Any, Self, override

class SubAddrId(ManagedObj):
  @staticmethod
  def generate(
    account: int,
    address: int
  ) -> Self:
    obj = blsct.gen_sub_addr_id(account, address);
    return SubAddrId(obj)

  @override
  def value(self) -> Any:
    return blsct.cast_to_sub_addr_id(self.obj)

